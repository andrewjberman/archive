<task_order>
  <metadata>
    <id>ADVI_INFINC.003</id>
    <slug>dsd-pattern-b-timeseries-append</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-05-15</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED — INFINC.002 RAVC2 received (649617a58). Phase 3 authorized.</dispatch_unblock_condition>
    <project_code>ADVI_INFINC</project_code>
    <priority>P1 — INF_C_02 client_performance is the central upstream for all D-stage scripts; append-only eliminates full 1,750-partition rebuild daily</priority>
    <sla>~2-3h wall actual per Pod 4 velocity</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inf-incremental-pipeline-design-20260514.md §2.2 (Pattern B mechanics)</ref>
    <ref type="phase2">ADVI_INFINC.002 RAVC2 (649617a58) — Pattern A complete; Phase 3 authorized</ref>
    <ref type="cto_q6">CTO Q6 ruling 2026-05-14: PK-stable sort + dedupe on write = Pattern B validation contract</ref>
    <ref type="lib_phase1">data/orion/scripts/gold/lib/skip_gate.py — NOT used in Pattern B (blob-level gate is script-internal); schema_version.py IS used</ref>
  </references>

  <context>
    Pattern B = cumulative timeseries blob append-only. Two scripts currently rebuild from all historical partitions on every run:

    INF_C_02 client_performance:
      Current: lists ~1,750 canonical_performance partitions, reads each, concat → single blob → s3://opal-data-inf/gold/timeseries/client_performance.parquet
      Target: read existing blob → find existing_max_date → read only new canonical_performance partitions (dates > existing_max_date) → append + dedupe(PK) + write back

    INF_C_03 account_performance:
      Same pattern. Output: s3://opal-data-inf/gold/timeseries/account_performance.parquet

    Why this matters: client_performance.parquet is the central upstream for the entire D-stage (INF_D_00, INF_D_02, etc.). The D-group run chain fires C_02 before D-layer. Making C_02 append-only directly reduces D-group chain wall time.

    Pattern B gate (script-internal, not skip_gate lib):
      1. Try to read existing blob from S3. If blob absent (first run / rebuild): fall through to full rebuild.
      2. Find existing_max_date = blob['date'].max()
      3. Identify new canonical partitions: dates > existing_max_date from gold/canonical_performance/
      4. If no new dates: log SKIP + exit 0 (nothing to do)
      5. If new dates: read only those partitions → append to existing blob → dedupe by PK → PK-stable sort → write back

    Schema version guard:
      Before appending, compare current script schema version vs blob metadata (gold/meta/schemas/INF_C_02.json + INF_C_03.json). If schema version bumped: FULL REBUILD (not append). Use schema_version.py from Phase 1 lib.

    Idempotence:
      Dedupe by PK on write handles reruns. PK: INF_C_02 = (date, household_id); INF_C_03 = (date, account_id). Use pd.concat(..., sort=False) to tolerate NaN-fill on new columns.

    Rebuild flag:
      os.environ.get('INFINC_REBUILD') == 'true' → skip blob-read, do full rebuild (same --rebuild passthrough as Pattern A).
  </context>

  <objective>
    Migrate INF_C_02 and INF_C_03 to append-only pattern: read existing blob, append only new-date rows, dedupe by PK, write back. Schema version guard forces full rebuild on column adds.
  </objective>

  <scope>
    <files>
      <file action="modify">data/orion/scripts/gold/INF_C_02.client_performance.py — Pattern B append gate + schema version guard</file>
      <file action="modify">data/orion/scripts/gold/INF_C_03.account_performance.py — Pattern B append gate + schema version guard</file>
      <file action="readonly_reference">data/orion/scripts/gold/lib/schema_version.py — Phase 1 schema version tracking lib</file>
      <file action="readonly_reference">docs/briefs/inf-incremental-pipeline-design-20260514.md §2.2 — Pattern B specification</file>
    </files>
  </scope>

  <phase id="0" when="before write — I/O surface">
    <step>
      <run>comp-pipescript io INF_C_02 — confirm: (a) output blob S3 path for existing blob read, (b) input canonical_performance partition path pattern, (c) any downstream consumers of client_performance.parquet blob.</run>
      <expect>Output path confirmed. Partition path pattern identified. D-stage consumer list noted.</expect>
    </step>
    <step>
      <run>comp-pipescript io INF_C_03 — same for account_performance.parquet.</run>
      <expect>I/O surface mapped for both scripts.</expect>
    </step>
    <step>
      <run>Read INF_C_02 current main loop — identify: (a) how canonical_performance partitions are listed, (b) where the blob write occurs, (c) current PK/sort order on write.</run>
      <expect>Loop structure understood. Insertion points for append gate identified.</expect>
    </step>
  </phase>

  <phase id="1" when="implementation — INF_C_02 first, then INF_C_03">
    <step>
      <run>INF_C_02 Pattern B migration:
        1. Import schema_version.py. Set SCHEMA_VERSION constant at top of file.
        2. In main(): attempt s3_read of existing blob. If absent or INFINC_REBUILD=true or schema version mismatch: full rebuild path (existing behavior).
        3. Append path: find existing_max_date, list canonical_performance partitions for dates > existing_max_date.
        4. If no new dates: log SKIP + exit 0.
        5. If new dates: read new partitions, pd.concat([existing_blob, new_rows], sort=False), dedupe by (date, household_id) keeping last, sort_values(['date', 'household_id']).
        6. Write back to same S3 path.
        7. Update schema version stamp in gold/meta/schemas/INF_C_02.json.
      ds-commit-gate.sh INF_C_02 before proceeding to C_03.</run>
      <expect>Append gate clean. Schema version guard wired. 3-gate PASS.</expect>
      <if_mismatch>Fix INF_C_02 before touching INF_C_03. Serial discipline.</if_mismatch>
    </step>
    <step>
      <run>INF_C_03 account_performance: same Pattern B migration. PK = (date, account_id). sort_values(['date', 'account_id']). ds-commit-gate.sh INF_C_03.</run>
      <expect>Append gate clean. 3-gate PASS.</expect>
    </step>
  </phase>

  <phase id="2" when="validation">
    <step>
      <run>Append validation: run INF_C_02 in append mode against a test date window (e.g., add 1 synthetic new date manually or use a date range where only 1 new partition exists). Verify: (a) existing blob rows unchanged (compare sample rows pre/post for dates in existing_max_date - 30d range), (b) new date rows present in output blob, (c) no duplicate rows by PK.</run>
      <expect>Existing rows byte-equal. New date present. No duplicates.</expect>
    </step>
    <step>
      <run>Skip validation: run INF_C_02 when existing_max_date == today. Expect: SKIP logged, blob unchanged, exit 0.</run>
      <expect>Skip fires correctly on up-to-date blob.</expect>
    </step>
    <step>
      <run>Schema version bump simulation: temporarily increment SCHEMA_VERSION constant. Run INF_C_02. Expect: full rebuild path taken (not append), schema stamp updated.</run>
      <expect>Schema guard triggers full rebuild on version bump.</expect>
    </step>
    <step>
      <run>Repeat append + skip validation for INF_C_03.</run>
      <expect>Same pass criteria.</expect>
    </step>
  </phase>

  <phase id="3" when="commit + deploy">
    <step>
      <run>safe-commit.sh --author "0.4.0_DS_ClientPlatform~D &lt;0.4.0_DS_ClientPlatform~D@opal.agent&gt;" -m "feat(INFINC.003): Pattern B append-only migration — INF_C_02/C_03 timeseries blobs" -- data/orion/scripts/gold/INF_C_02.client_performance.py data/orion/scripts/gold/INF_C_03.account_performance.py</run>
      <expect>Commit clean. No contamination.</expect>
    </step>
    <step>
      <run>safe-deploy.sh — push CLOUD + S3 upload + comp-pipescript deployed MATCH for INF_C_02 + INF_C_03.</run>
      <expect>SHA-MATCH on both. Deploy clean.</expect>
    </step>
    <step>
      <run>SSM-direct INF_C_02 append run. Observe wall time vs pre-migration baseline. Log skip count + new-date write confirmation.</run>
      <expect>Wall time materially reduced vs full-rebuild baseline. New-date written. Historical skipped.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + AE 0.6.1 with: commit SHA, deploy MATCH, append validation evidence, wall-time comparison, skip validation pass.</run>
      <expect>Evidence-bearing RAVC2. Phase 4+ authorized post-RAVC2.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: INF_C_02 reads existing blob and appends only new-date rows (not full rebuild) when blob exists and is up-to-date
    AC2: INF_C_03 same Pattern B append gate
    AC3: Dedupe by PK on write (INF_C_02: (date, household_id); INF_C_03: (date, account_id)); no duplicate rows
    AC4: PK-stable sort pre-write (INF_C_02: ['date','household_id']; INF_C_03: ['date','account_id'])
    AC5: Schema version guard: if SCHEMA_VERSION bumped vs gold/meta/schemas/{script}.json → full rebuild
    AC6: INFINC_REBUILD=true passthrough → full rebuild (same as Pattern A)
    AC7: Skip path: if existing_max_date == today → SKIP + exit 0
    AC8: Absent blob (first run) → full rebuild (no crash)
    AC9: ds-commit-gate.sh 3-gate PASS on both scripts
    AC10: from __future__ import annotations preserved as first import (Rule 15)
    AC11: safe-deploy.sh PASS + comp-pipescript deployed MATCH on both scripts
    AC12: Append validation: existing rows unchanged + new date rows present + no duplicates
    AC13: Wall-time reduction demonstrated empirically (INF_C_02 SSM run)
    AC14: No emoji per CLAUDE.md
    AC15: RAVC2 to COO + CC CTO + AE 0.6.1
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 0 comp-pipescript io x2; Phase 1 ds-commit-gate.sh x2; Phase 3 comp-pipescript deployed x2; safe-deploy.sh.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCY: INFINC.002 RAVC2 (649617a58) — COMPLETE.
    AE 0.6.1: CC on RAVC2; INF_C_02 is central upstream for D-stage; wall-time reduction will cascade to all D-group chain runs.
    DOWNSTREAM: Phase 4 (Pattern C: per-HH historical-replay artifacts, INF_D_06) gates on this RAVC2.
    NO PLATINUM SHAPE CHANGE: blob schema unchanged; downstream D-stage consumers unaffected by append vs rebuild.
  </cross_domain_coordination>

  <notes>
    **Serial discipline:** INF_C_02 first (higher impact, D-stage upstream). ds-commit-gate.sh PASS before touching INF_C_03.

    **Existing blob read:** use pd.read_parquet(s3_path) with same S3 client pattern as rest of script. If S3 raises NoSuchKey → full rebuild path.

    **pd.concat sort=False:** required to tolerate NaN-fill on new columns. Do not use sort=True (reorders columns alphabetically, breaks downstream shape contracts).

    **Schema version lib:** use schema_version.py from Phase 1. Store stamp at gold/meta/schemas/INF_C_02.json and gold/meta/schemas/INF_C_03.json.

    **No emoji per CLAUDE.md.**

    **Author identity:** --author="0.4.0_DS_ClientPlatform~D &lt;0.4.0_DS_ClientPlatform~D@opal.agent&gt;".
  </notes>
</task_order>
