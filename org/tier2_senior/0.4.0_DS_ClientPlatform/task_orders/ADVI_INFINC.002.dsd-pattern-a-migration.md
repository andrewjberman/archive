<task_order>
  <metadata>
    <id>ADVI_INFINC.002</id>
    <slug>dsd-pattern-a-migration</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-05-15</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>DS~D INFFIN.021 RAVC2 close. Phase 1 (.001) RAVC2 already complete (d88b7a7a4 + 64e583272 + f45f01460).</dispatch_unblock_condition>
    <project_code>ADVI_INFINC</project_code>
    <priority>P1 — Pattern A migration; gates 35-40 min/day chain waste elimination</priority>
    <sla>~2-4h wall actual per Pod 4 velocity (brief baseline: ~5 dev-days DS~B)</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inf-incremental-pipeline-design-20260514.md §2.1 + §5.2 + §6 Q6 ruling</ref>
    <ref type="phase1">ADVI_INFINC.001 (complete — skip_gate.py + empty_sentinel.py + dispatch.sh flags shipped)</ref>
    <ref type="andrew_direct">Andrew 2026-05-14 live chain: "make a truly incremental version of this flow rather than having to rebuild 7 years of history every single day"</ref>
    <ref type="redirect">Phase 2-6 routed DS~C + DS~D per Andrew direct (per INFINC.001 redirect history)</ref>
    <ref type="cto_q6">CTO Q6 ruling 2026-05-14: PK-stable sort on write + byte-equal (md5) validation contract for Pattern A migrations</ref>
  </references>

  <context>
    Phase 1 shipped the skip_gate lib + empty_sentinel + dispatch.sh flags. Phase 2 migrates the 5 Pattern A scripts to consume should_skip() at their partition loops — the highest-value waste elimination in the chain.

    Pattern A = date-partitioned canonical outputs. Each script currently walks ALL historical date partitions and rewrites every output file unconditionally. Post-migration: should_skip() returns True for past partitions where output exists AND silver inputs haven't changed AND no schema bump AND --rebuild not set. Only new-date partitions (and any explicitly flagged) write.

    5 Pattern A scripts, ordered by wall-time savings priority:
    1. INF_B_00 canonical_holdings — 10.6 min daily; highest priority
    2. INF_B_03 account_gains — 5 min daily
    3. INF_C_00 canonical_performance — 6.5 min daily
    4. INF_C_01 canonical_nna — 50s (also exercises signal-bounded empty_sentinel pattern)
    5. INF_A_03 positions_cube — touched on chain

    Expected steady-state gain from Pattern A alone: ~22-23 min/day recovered (B_00 10.6 + B_03 5 + C_00 6.5 + remainder).

    CTO Q6 ruling: for Pattern A, post-vs-pre numeric diff per partition must be zero (same computation on same inputs). PK-stable sort on write + byte-equal md5 validation is the contract.

    PK sort order per script (brief §6):
    - INF_B_00: (date, account_id, ticker)
    - INF_B_03: (date, account_id, ticker)
    - INF_A_03: (date, account_id, ticker)
    - INF_C_00: (date, account_id)
    - INF_C_01: (date, account_id)
  </context>

  <objective>
    Migrate 5 Pattern A scripts to use should_skip() per-partition gate. Each script: (1) import lib, (2) call should_skip() at partition loop start, (3) add PK-stable sort pre-write. Validate byte-equal on historical partitions post-migration.
  </objective>

  <scope>
    <files>
      <file action="modify">data/orion/scripts/gold/INF_B_00.canonical_holdings.py — should_skip() at partition loop + PK sort</file>
      <file action="modify">data/orion/scripts/gold/INF_B_03.account_gains.py — should_skip() at partition loop + PK sort</file>
      <file action="modify">data/orion/scripts/gold/INF_C_00.canonical_performance.py — should_skip() at partition loop + PK sort</file>
      <file action="modify">data/orion/scripts/gold/INF_C_01.canonical_nna.py — should_skip() + empty_sentinel pattern</file>
      <file action="modify">data/orion/scripts/gold/INF_A_03.positions_cube.py — should_skip() at partition loop + PK sort</file>
      <file action="readonly_reference">data/orion/scripts/gold/lib/skip_gate.py — Phase 1 artifact (should_skip signature)</file>
      <file action="readonly_reference">data/orion/scripts/gold/lib/empty_sentinel.py — Phase 1 artifact (mark_empty / is_empty)</file>
    </files>
  </scope>

  <phase id="0" when="before write — signature verify">
    <step>
      <run>Read lib/skip_gate.py should_skip() signature; note exact parameter names (script_id, partition_date, output_key, silver_input_keys). Confirm lib is on S3 and deployed (comp-pipescript deployed skip_gate).</run>
      <expect>Signature confirmed; lib deployed and accessible to script imports at runtime.</expect>
      <if_mismatch>If lib not deployed: safe-deploy.sh on lib files before proceeding. Do not import a lib that isn't on S3.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io INF_B_00 — identify: (a) which silver input keys the script reads, (b) the output partition key pattern, (c) the main date-loop variable name.</run>
      <expect>I/O surface mapped. silver_input_keys list for should_skip() call at INF_B_00 identified.</expect>
    </step>
    <step>
      <run>Repeat comp-pipescript io for INF_B_03 + INF_C_00 + INF_C_01 + INF_A_03.</run>
      <expect>All 5 script I/O surfaces mapped; silver_input_keys lists ready for each should_skip() call.</expect>
    </step>
  </phase>

  <phase id="1" when="implementation — serial per script">
    <step>
      <run>INF_B_00: Add `from gold.lib.skip_gate import should_skip` import. At partition loop start: `if should_skip("INF_B_00", date, output_key, silver_input_keys): continue`. Before .to_parquet(): sort_values(["date","account_id","ticker"]). ds-commit-gate.sh INF_B_00.</run>
      <expect>Gate-and-continue pattern clean. PK sort present. ds-commit-gate.sh 3-gate PASS.</expect>
      <if_mismatch>Fix before moving to INF_B_03. Serial discipline — do not stack broken scripts.</if_mismatch>
    </step>
    <step>
      <run>INF_B_03: Same pattern. silver_input_keys = holdings partitions that B_03 reads. PK sort (date, account_id, ticker). ds-commit-gate.sh INF_B_03.</run>
      <expect>Gate-and-continue clean. PK sort present. 3-gate PASS.</expect>
    </step>
    <step>
      <run>INF_C_00: Same pattern. silver_input_keys = holdings/perf partitions. PK sort (date, account_id). ds-commit-gate.sh INF_C_00.</run>
      <expect>Gate-and-continue clean. 3-gate PASS.</expect>
    </step>
    <step>
      <run>INF_C_01: should_skip() + empty_sentinel pattern (brief §4.2): if no NNA records for a date → mark_empty("INF_C_01", date) instead of writing empty parquet; is_empty() gate at loop start. PK sort (date, account_id). ds-commit-gate.sh INF_C_01.</run>
      <expect>Gate + empty_sentinel clean. 3-gate PASS.</expect>
    </step>
    <step>
      <run>INF_A_03: Same Pattern A. PK sort (date, account_id, ticker). ds-commit-gate.sh INF_A_03.</run>
      <expect>Gate-and-continue clean. 3-gate PASS.</expect>
    </step>
  </phase>

  <phase id="2" when="validation">
    <step>
      <run>Select 3 historical partition dates from each script (e.g., 2024-07-20, 2024-01-15, 2023-06-01). For each: (a) download current S3 partition, (b) compute md5 of sorted output, (c) run script in --dry-run-check mode OR compare against pre-migration snapshot. Verify byte-equal per CTO Q6 ruling.</run>
      <expect>All historical partitions byte-equal pre/post migration. Zero numeric diff. md5 MATCH on 3 sample dates per script = 15 checks total.</expect>
      <if_mismatch>STOP. Byte-equality failure = bug in skip logic or PK sort. Diagnose before commit. Do not proceed to safe-deploy with a failing validation.</if_mismatch>
    </step>
    <step>
      <run>New-date check: confirm script DOES write the new partition (today's date) when should_skip() returns False for a non-existent output key.</run>
      <expect>New partition written correctly; skip gate only fires on existing outputs.</expect>
    </step>
  </phase>

  <phase id="3" when="commit + deploy">
    <step>
      <run>safe-commit.sh --author "0.4.0_DS_ClientPlatform~D &lt;0.4.0_DS_ClientPlatform~D@opal.agent&gt;" -m "feat(INFINC.002): Pattern A skip-gate migration — INF_B_00/B_03/C_00/C_01/A_03" -- data/orion/scripts/gold/INF_B_00.canonical_holdings.py data/orion/scripts/gold/INF_B_03.account_gains.py data/orion/scripts/gold/INF_C_00.canonical_performance.py data/orion/scripts/gold/INF_C_01.canonical_nna.py data/orion/scripts/gold/INF_A_03.positions_cube.py</run>
      <expect>Commit clean. No contamination.</expect>
    </step>
    <step>
      <run>safe-deploy.sh per Rule 13: push to CLOUD → S3 upload → comp-pipescript deployed MATCH for all 5 scripts.</run>
      <expect>SHA-MATCH on all 5; deploy clean.</expect>
    </step>
    <step>
      <run>SSM-direct --single INF_B_00 on today's date only. Observe wall time vs pre-migration baseline (expect &lt;1 min vs 10.6 min). Confirm new-date partition written; historical partitions skipped (log skip count).</run>
      <expect>Wall time &lt;1 min. Skip count = (total historical partitions - 1). New partition written.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + AE 0.6.1 with: commit SHA, safe-deploy log, wall-time comparison (B_00 only empirical + projected B_03/C_00/C_01/A_03 by pattern), md5 byte-equal sample evidence.</run>
      <expect>Evidence-bearing RAVC2. Phase 3 (Pattern B) dispatch authorized post-RAVC2.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: All 5 Pattern A scripts have should_skip() gate at partition loop start
    AC2: All 5 scripts have PK-stable sort pre-write (per CTO Q6 ruling)
    AC3: INF_C_01 additionally uses empty_sentinel pattern per brief §4.2
    AC4: ds-commit-gate.sh 3-gate PASS on all 5 scripts
    AC5: Byte-equal validation PASS on 3 sample historical dates per script (15 checks)
    AC6: New-date partition write confirmed (skip gate does not block new dates)
    AC7: safe-deploy.sh PASS + comp-pipescript deployed MATCH on all 5 scripts
    AC8: INF_B_00 empirical SSM-direct wall-time improvement demonstrated (&lt;1 min vs 10.6 min baseline)
    AC9: from __future__ import annotations preserved as first import per Rule 15
    AC10: No emoji per CLAUDE.md
    AC11: RAVC2 to COO + CC CTO + AE 0.6.1 with wall-time evidence
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 0 comp-pipescript io x5; Phase 1 ds-commit-gate.sh x5; Phase 2 comp-pipescript deployed x5; Phase 3 safe-deploy.sh.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: INFINC.001 Phase 1 RAVC2 (complete). DS~D INFFIN.021 RAVC2 (dispatch_held until this closes).
    PARALLEL-OK: DS~C INFFIN.019 investigation; DS~A ECLDAT.002; RD INFFIN Wave 1.
    DOWNSTREAM: Phase 3 (Pattern B: C_02/C_03 append-only timeseries) gates on this RAVC2.
    AE 0.6.1 CC on RAVC2 for chain-integration awareness — AE owns dispatch.sh; any dispatch.sh interaction from should_skip() behavior should be confirmed with AE.
    NO PRODUCTION BEHAVIOR CHANGE for consumers: platinum outputs unchanged in shape; only gold internal partition reuse changes.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <note>Pattern A migration is gold-side internal only. Platinum outputs unchanged. No silver re-emit. No Lambda redeploy. If byte-equal validation passes (AC5), consumer contracts are preserved by construction. Full --rebuild available via dispatch.sh flag (Phase 1 deliverable) if any downstream observes unexpected behavior.</note>
  </data_reprocess_scope>

  <deliverables>
    1. 5 Pattern A scripts with should_skip() gates + PK sort
    2. INF_C_01 empty_sentinel wiring
    3. ds-commit-gate.sh PASS evidence (5 scripts)
    4. Byte-equal validation (15 sample checks)
    5. safe-deploy.sh + S3 SHA-MATCH
    6. INF_B_00 empirical wall-time comparison
    7. RAVC2 with full evidence set
  </deliverables>

  <ravc>DS~D RAVC2 to COO + CC CTO + AE 0.6.1 on AC1-11 PASS. Phase 3 (Pattern B) dispatch authorized post-RAVC2.</ravc>

  <notes>
    **Author identity:** `--author="0.4.0_DS_ClientPlatform~D &lt;0.4.0_DS_ClientPlatform~D@opal.agent&gt;"`.

    **Serial migration discipline:** migrate INF_B_00 first (highest wall-time value). Get ds-commit-gate.sh PASS before moving to next script. Do not batch 5 scripts in parallel — a bug in the skip_gate call signature discovered at B_00 propagates cleanly if caught before B_03 is written.

    **Lib import path:** use the path convention established in Phase 1. If Phase 1 used `from lib.skip_gate import should_skip` (relative), use the same convention across all 5 scripts.

    **--rebuild passthrough:** confirm `os.environ.get("INFINC_REBUILD") == "true"` or equivalent flag from dispatch.sh is visible inside the script; should_skip() returns False when --rebuild set (per Phase 1 lib contract).

    **Byte-equal validation methodology:** simplest correct approach — download current S3 partition → pd.read_parquet → sort_values(pk) → df.to_parquet(buf) → md5(buf). After migration, re-run same path on the new output. Hashes must match. If they don't, the migration introduced a behavioral change (investigate before RAVC2).

    **Phase 3 preview (not scope here):** Pattern B = cumulative timeseries blob append-only (INF_C_02 client_performance, INF_C_03 account_performance). Different pattern — blob is assembled from all partitions; append-only means new partitions are appended to blob rather than full-rebuild. Phase 3 TO authors post-RAVC2 of this TO.

    **No emoji per CLAUDE.md.**
  </notes>
</task_order>
