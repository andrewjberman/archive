<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.INF_A_03_PARALLEL-EXPAND</id>
    <project>ADVI_INFNNA</project>
    <title>INF_A_03.positions_cube — port BD's ProcessPool + numpy-array expand + parallel S3 write; eliminate per-(account,ticker) iterrows() loop</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>DRAFT-2026-05-11</issued_date>
    <status>staged</status>
    <priority>high</priority>
    <estimated_effort>~3-4h (port + dry-run + parity validation + cascade)</estimated_effort>
    <authorized_by>DRAFT — pending COO ratification of A-GROUP-AUDIT findings RAVC4 2026-05-11</authorized_by>
  </metadata>

  <references>
    <ref type="parent_audit">A-GROUP-AUDIT findings doc `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-11/DS_B_a_group_audit_findings.md` Finding #1 (and #3 + #6 — bundled here)</ref>
    <ref type="reference_pattern">BD A_03 ProcessPool + numpy expand: `data/black_diamond/scripts/gold/A_03.positions_cube.py:1036-1162` (`_expand_one_pair` module-level fn, `expand_pairs_to_daily` orchestrator with `ProcessPoolExecutor(max_workers=EXPAND_WORKERS)`)</ref>
    <ref type="reference_pattern">BD A_03 parallel S3 write: same file, `S3_WRITE_WORKERS = int(os.environ.get('O2_WRITE_WORKERS', '0')) or 64`</ref>
    <ref type="affected_script">data/orion/scripts/gold/INF_A_03.positions_cube.py</ref>
    <ref type="telemetry_baseline">Friday `.runtmp/telemetry/2026-05-08/inf-gold-layer-runner/INF_A_03.positions_cube/v006-192400Z-bb954100eebf.jsonl` — 583.1s wall, 3,362MB peak, 689.9% cpu_max, 89.2% cpu_p50</ref>
  </references>

  <context>
    INF_A_03 is 14% of total cascade wall-clock (583s of ~4,140s on Friday's instrumented cascade). The lead cost is a sequential Python loop:

    ```
    for (acct_id, tkr), grp in chunk.groupby(['account_id', 'ticker']):
        grp.set_index/reindex/ffill/loc/iterrows -> append dict to date_buffers
    ```

    With ~33K (account, ticker) pairs × ~2,180 days, this produces ~29M `iterrows()` calls. Friday telemetry confirms cpu_p50=89% (single-core median) while cpu_max=689.9% comes only from the upstream 64-thread S3 read phase.

    BD A_03 solved this exact problem with `ProcessPoolExecutor` + numpy-array expansion (`_expand_one_pair`). Production-validated pattern; the port to INF is mechanical.

    Bundled into this TO (per audit findings doc):
    - **Finding #1**: ProcessPool numpy-expand (lead win)
    - **Finding #3**: parallel S3 write via `S3_WRITE_WORKERS` (small additional win, same surface)
    - **Finding #6**: explicit elimination of `iterrows()` (subsumed by Finding #1)
    - **Finding #7**: drop dead `MIN_OUTPUT_DATE='2019-09-01'` constant OR convert to env-var matching BD pattern

    NOT bundled (separate TOs if ratified):
    - Finding #2 (txn-cache shared across A_00/A_01/A_03) — different surface
    - Finding #4 (stale 247 keys) — one-time hygiene, separate TO
    - Finding #5 (A_02 retire) — different script
  </context>

  <scope>
    <step>
      Port BD's `_expand_one_pair` module-level fn into `data/orion/scripts/gold/INF_A_03.positions_cube.py`. Keep BD's signature exactly: `(account_id, ticker, trade_dates_ns, cum_units, end_date_ns, expand_start_ns) -> (account_id, ticker, dates_out, units_out)`. Use numpy `searchsorted` + `take` for forward-fill. NO pandas inside the worker.
    </step>

    <step>
      Replace the `for (acct_id, tkr), grp in chunk.groupby(...)` loop in `build_positions_cube` with a `ProcessPoolExecutor(max_workers=EXPAND_WORKERS)` orchestrator that maps work items per (account, ticker) pair. Use `chunksize=64` like BD. On Windows (DS dev box), keep BD's `_USE_PROCESS_POOL = (os.name != 'nt')` guard so dev runs fall back to ThreadPool.
    </step>

    <step>
      Replace the sequential `for dt_str in sorted(date_buffers): s3.put_object(...)` write with `ThreadPoolExecutor(max_workers=S3_WRITE_WORKERS)` (S3_WRITE_WORKERS env-var defaults to 64, mirror BD).
    </step>

    <step>
      Drop dead `MIN_OUTPUT_DATE = '2019-09-01'` constant — silver/transactions earliest is 2020-05-26, so the constant has zero functional impact today. Either delete OR convert to env-var `INF_MIN_OUTPUT_DATE` matching BD's `O2_MIN_OUTPUT_DATE` pattern. Recommend delete + add to docstring as "implicit min = silver/transactions earliest trade_date".
    </step>

    <step>
      Pre-commit gate: `.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_A_03.positions_cube.py` — must exit 0.
    </step>

    <step>
      Parity validation: dry-run the new INF_A_03 against the deployed version on 5 spot-check dates (2020-06-10, 2022-01-15, 2024-06-30, 2026-05-01, 2026-05-07). For each date, compare output parquet row-by-row sorted by (account_id, ticker, units). Must be byte-identical (modulo row order — sort post-hoc).
    </step>

    <step>
      QA cascade: dispatch `inf-gold-qa-runner` SSM with `--from INF_A_03 --to INF_A_03` scope to capture new telemetry. Compare to Friday baseline:
      - wall_s: target &lt; 180s (vs Friday 583s)
      - mem_peak_mb: target &lt; 2,000MB (vs Friday 3,362MB)
      - cpu_p50: target &gt; 400% (vs Friday 89%)
      - output parity: 0 cell diffs across 5 spot-check dates
    </step>

    <step>
      If parity + telemetry targets met: commit, push, S3 upload via DS-direct (`aws s3 cp` to `s3://opal-data-inf/code/gold/`), `comp-pipescript deployed INF_A_03` MATCH verify.
    </step>

    <step>
      Full E2E re-cascade via SSM dispatch to confirm downstream B/C/D scripts consume the new positions_cube without regression. Capture telemetry; compare A_03 line in distribution to Friday.
    </step>
  </scope>

  <acceptance_criteria>
    1. `INF_A_03.positions_cube.py` ports BD's `_expand_one_pair` + ProcessPool orchestrator + parallel S3 write.
    2. Pre-commit gate (`ds-commit-gate.sh`) exits 0.
    3. Parity: 5 spot-check dates byte-identical (sorted) to current deployed cube.
    4. Telemetry: A_03 wall_s &lt; 180s, peak mem &lt; 2,000MB, cpu_p50 &gt; 400% on instrumented QA cascade.
    5. E2E re-cascade: zero downstream regressions; D-layer artifacts unchanged.
    6. Session log captures: pre-/post telemetry comparison table, parity check results, commit SHA, S3 ETag, MATCH verification.
    7. RAVC2/4 to COO with savings delta in seconds + percentage of cascade.
    8. `comp-validate INF_A_03 --artifact /tmp/positions_cube_test.parquet` exit 0 (if validate config exists; else N/A noted).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>`comp-pipescript io INF_A_03`</run><expect>COLUMN GAPS report on read columns; if INF gold catalog isn't fully wired, fall back to source read.</expect></step>
      <step><run>`comp-blast INF_A_03.positions_cube` (or `gold/positions_cube` artifact)</run><expect>Downstream B_00, B_01, C_00, C_01, D_* enumerated. Confirm no surprise consumer.</expect></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>`.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_A_03.positions_cube.py`</run><expect>Exit 0 — py_compile + AST undefined-name + ruff all clean.</expect></step>
      <step><run>Local dry-run parity check on 5 spot-check dates</run><expect>Byte-identical (sorted by account_id, ticker, units).</expect></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>`comp-pipescript deployed INF_A_03`</run><expect>MATCH after `aws s3 cp` to `s3://opal-data-inf/code/gold/`.</expect></step>
      <step><run>SSM scoped QA cascade + telemetry analyze</run><expect>wall_s &lt; 180s, peak mem &lt; 2GB, cpu_p50 &gt; 400%.</expect></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None. Independent — INF_A_03 source change is contained. No upstream gate.
  </dependencies>

  <next>On commit + telemetry pass: A-layer wall-clock drops by ~7-8 min per cascade (40% of A-layer total). COO can author follow-up TXN-CACHE TO independently.</next>

  <draft_note>
    Authored DRAFT by 0.4.0_DS_ClientPlatform~B 2026-05-11 per AC9 scope-creep guard (no implementation in A-GROUP-AUDIT). Awaiting COO ratification + dispatch. Status remains `staged` until COO flip to `pending` + GO message.
  </draft_note>
</task_order>
