<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.INF_A_LAYER_TXN-CACHE</id>
    <project>ADVI_INFNNA</project>
    <title>INF A-layer — eliminate triple silver/transactions read across A_00/A_01/A_03 via shared in-memory cache OR materialized intermediate</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>DRAFT-2026-05-11</issued_date>
    <status>staged</status>
    <priority>medium</priority>
    <estimated_effort>~2h (architecture + per-script wiring + cascade validation)</estimated_effort>
    <authorized_by>DRAFT — pending COO ratification of A-GROUP-AUDIT findings RAVC4 2026-05-11</authorized_by>
  </metadata>

  <references>
    <ref type="parent_audit">A-GROUP-AUDIT findings doc Finding #2 — triple-load of silver/transactions</ref>
    <ref type="affected_scripts">data/orion/scripts/gold/INF_A_00.accounts_dimension.py, INF_A_01.advisor_assignments.py, INF_A_03.positions_cube.py</ref>
    <ref type="telemetry_baseline">Friday A_00=26.8s + A_01=27.1s + A_03 read-phase ~27s = ~80s of duplicated I/O per cascade</ref>
  </references>

  <context>
    A_00, A_01, and A_03 each independently fan out a 64-thread S3 read of all 1,510 silver/transactions/{date}.parquet partitions. Since they read overlapping (and largely identical) column subsets, this is ~60s of duplicated I/O per cascade.

    Two viable architectures:

    **Option A (preferred — simpler):** Materialized intermediate. Add a new `INF_A_-1.materialize_txn_cache.py` step at cascade entry that reads silver/transactions/ once and writes a single concatenated parquet to `/tmp/inf_silver_txn_cache.parquet` (or `gold/_cache/silver_txn_cache.parquet` if shared across processes is needed). A_00/A_01/A_03 read from the local file (~1s) instead of S3 fan-out.

    **Option B:** Shared library function. `lib/silver_txn_loader.py` with module-level cache `_TXN_CACHE`. A_00/A_01/A_03 import + call once per process. Won't help if scripts run in separate Python processes (which they do per cascade).

    Recommend Option A for the cascade-runner case (separate processes per script).

    Trade-off: adds one step + ~30s for the materialize phase, but saves ~60s across A_00+A_01+A_03 reads. Net ~30s savings per cascade. Real win is when combined with INF_A_03_PARALLEL-EXPAND (this TO + that TO together drop A-layer wall-clock from ~660s → ~150s, a 4.4x speedup).

    Lower priority than INF_A_03_PARALLEL-EXPAND because the per-script cost is moderate; do this AFTER A_03 lands so we don't fight merge conflicts.
  </context>

  <scope>
    <step>
      Author `data/orion/scripts/gold/INF_A_-1.materialize_txn_cache.py` — single-shot materializer:
      - Read silver/transactions/{date}.parquet × 1,510 with `ThreadPoolExecutor(max_workers=64)`
      - Concat into single dataframe; write to `/tmp/inf_silver_txn_cache.parquet` with snappy compression
      - Optionally also upload to `s3://opal-data-inf/gold/_cache/silver_txn_cache.parquet` for cross-process reuse (decide based on EC2 runner shape)
      - CLI: `--upload`, `--dry-run`, `--cache-path` (defaults to /tmp)
      - Sized: ~1,510 partitions × ~50KB each = ~75MB cache file
    </step>

    <step>
      Add a shared loader helper in `data/orion/scripts/gold/lib/txn_cache_reader.py`:
      - `load_cached_transactions(columns=None, date_filter_start=None, date_filter_end=None) -> pd.DataFrame`
      - Reads from `/tmp/inf_silver_txn_cache.parquet` if present
      - Falls back to S3 fan-out if cache missing (preserves stand-alone script invocation)
      - Logs which path was used (cache hit / fan-out fallback)
    </step>

    <step>
      Update INF_A_00.load_transactions to use `txn_cache_reader.load_cached_transactions(KEEP_COLS)`. Single-call replacement; keep the column subset filter behavior identical.
    </step>

    <step>
      Update INF_A_01.load_assignments to use `txn_cache_reader.load_cached_transactions(KEEP_COLS)`. Same shape replacement.
    </step>

    <step>
      Update INF_A_03.load_transactions to use `txn_cache_reader.load_cached_transactions(KEEP_COLS, date_filter_start, date_filter_end)`. Same shape; cache reader handles the date filter post-read.
    </step>

    <step>
      Pre-commit gate on every edited .py file (4-5 files): `.tools/ds-commit-gate.sh ...`
    </step>

    <step>
      Cascade orchestrator update — add INF_A_-1 as the first step before INF_A_00. If using cascade-runner manifest, prepend the entry. Capture timing.
    </step>

    <step>
      QA cascade: dispatch instrumented run of A-layer (INF_A_-1 → INF_A_04). Compare Friday baseline:
      - INF_A_-1 wall: expected ~30s (single shared read)
      - INF_A_00 wall: expected &lt; 5s (was 27s)
      - INF_A_01 wall: expected &lt; 5s (was 27s)
      - INF_A_03 read-phase: expected &lt; 2s (was ~27s)
      - Total A-layer wall (combined w/ INF_A_03_PARALLEL-EXPAND if shipped): target &lt; 200s vs Friday 660s
    </step>

    <step>
      Commit, push, S3 upload (DS-direct), comp-pipescript deployed MATCH on all 4 affected scripts + new INF_A_-1.
    </step>
  </scope>

  <acceptance_criteria>
    1. `INF_A_-1.materialize_txn_cache.py` ships + materializes successfully.
    2. `lib/txn_cache_reader.py` ships with cache-hit + fan-out-fallback paths both tested.
    3. INF_A_00 / INF_A_01 / INF_A_03 use shared loader.
    4. Pre-commit gate exits 0 on all .py edits.
    5. Telemetry: combined A_00 + A_01 + A_03-read wall &lt; 15s on QA cascade (vs Friday ~80s).
    6. Output parity: A_00 + A_01 + A_03 outputs byte-identical to current deployed.
    7. Stand-alone invocation still works (cache-miss path) — verify with `python INF_A_00.py --upload` from clean /tmp.
    8. `comp-pipescript deployed` MATCH on INF_A_-1, INF_A_00, INF_A_01, INF_A_03 post-upload.
    9. Session log captures pre-/post telemetry, parity, commit SHA, S3 ETags.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>`comp-blast` for each affected script</run><expect>No surprise downstream consumer; A_00/A_01/A_03 outputs unchanged.</expect></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>`.tools/ds-commit-gate.sh` on every .py file edited</run><expect>Exit 0 each.</expect></step>
      <step><run>Local materialize test + per-script load via cache</run><expect>Each script loads &lt; 5s when cache present; falls back when cache absent.</expect></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>`comp-pipescript deployed` for each script + new INF_A_-1</run><expect>MATCH each.</expect></step>
      <step><run>Cascade telemetry comparison</run><expect>A-layer total wall down by 60+ sec.</expect></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    Recommend: ship AFTER ADVI_INFNNA.INF_A_03_PARALLEL-EXPAND so A_03 is in its post-port shape when the cache wiring lands. Avoids merge conflict on the same load_transactions function.
  </dependencies>

  <next>On commit + telemetry pass: A-layer wall-clock down to ~150s (combined w/ A_03 port). COO can author hygiene follow-ups.</next>

  <draft_note>
    Authored DRAFT by 0.4.0_DS_ClientPlatform~B 2026-05-11 per AC9 scope-creep guard. Awaiting COO ratification + dispatch.
  </draft_note>
</task_order>
