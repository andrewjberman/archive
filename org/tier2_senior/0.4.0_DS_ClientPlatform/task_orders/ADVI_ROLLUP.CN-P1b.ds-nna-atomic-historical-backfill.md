<task_order>
  <metadata>
    <id>ADVI_ROLLUP.CN-P1b</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- COMPLETE 2026-04-16 14:29:27Z per DS~D MCP 15:15:38Z. Evidence: commit dc4980c3 (2,294 partitions, 9,245,944 rows, S3 count PASS). AC#7 CTO reinterp authorized MCP 14:36:47Z "legacy nna/ comparison satisfies intent" (activity-only C_03 gains-join diverges structurally; legacy nna/ shares identical nna_flows pipeline). Parity PASS on 4-date sample: 2026-04-13/2023-06-15/2021-12-31/2022-09-01, in_diff 0.00%, out_diff <=0.08%. AC2 90-date INV1/INV2/INV4/INV5 spot-check pending (CTO non-blocking for CN-P2). CN-P2 UNBLOCKED; DS~D proceeding Path B. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>4 (Structural convergence)</wave>
    <priority>P1 (HARD-blocks CN-P3 ~B refire + Wave 4 convergence gate)</priority>
  </metadata>

  <references>
    <ref type="trigger">~B Rule 7 pre-flag #2 + CTO redline 2026-04-15 21:48Z — nna_atomic has 1 partition (2026-04-13) vs legacy `gold/canonical/nna/` 2294 partitions; D_00c multi-window aggregations (3M/6M/1Y/2Y/3Y/MTD/QTD/YTD/MAX) collapse to ~99% data loss without backfill</ref>
    <ref type="prereq">ADVI_ROLLUP.CN-P1 — daily shadow writer (commit bf9651b8 + ~D RA-P1 6c0da968 close)</ref>
    <ref type="blocks">ADVI_ROLLUP.CN-P3 — D_00c leaderboard cutover (HELD pending this backfill)</ref>
    <ref type="related">ADVI_ROLLUP.CN-P4 — D_01 partner_analytics cutover (further downstream gate)</ref>
    <ref type="prd">docs/architecture/ADVI_CANNNA_PLAN.md</ref>
  </references>

  <objective>
    Backfill `gold/canonical/nna_atomic/{YYYY-MM-DD}.parquet` to match the legacy `gold/canonical/nna/` partition range. Without this, D_00c multi-window aggregations (and any other historical NNA window consumer) collapse to single-day sums when cut over to nna_atomic.

    **Window:** match the legacy `gold/canonical/nna/` partition list 1:1. Per CTO redline: ~2294 partitions back to ~2018. Cheap to over-backfill, expensive to under-backfill.

    **Source:** silver inflows/outflows historical. Same compute path as your CN-P1 daily writer. Per-date loop, partition-write to S3.

    **Validator:**
    - Partition count: `aws s3 ls s3://opal-data-bd/gold/canonical/nna_atomic/ | wc -l` ≥ `aws s3 ls s3://opal-data-bd/gold/canonical/nna/ | wc -l`
    - Spot-check sum-by-date parity against legacy nna source for ≥90 dates within $0.01 per date OR documented divergence reason (atomic semantics may legitimately diverge from legacy aggregate semantics — document if so).

    **CRITICAL — Rule 7 pre-flag MANDATORY before `aws s3 cp` / `--upload`** for bulk historical write. A→D-rerun-sensitive surface (your own memory rule applies).

    **Sequencing on ~D lane (RE-SEQUENCED per CTO Path B 2026-04-16 12:58Z):**
    1. **CN-P1b (this TO) — SHIPS FIRST.** Full ~2294 partition backfill of `gold/canonical/nna_atomic/`. Pre-dependency for every downstream NNA cutover.
    2. CN-P2 (D_02 consumer cutover) — staged behind CN-P1b, ships single-commit once CN-P1b data validated.
    3. RA-P1b — independent, can interleave.
    4. CN-P3/P4/P5 cutover cascade — gated on CN-P1b close (auto-clearable HOLDs).
  </objective>

  <scope>
    <files>
      <file action="create_or_extend">data/black_diamond/scripts/gold/C_01.{nna_atomic_backfill}.py (extend C_01 or write standalone)</file>
      <file action="reference_only">data/black_diamond/scripts/gold/D_00c.advisor_leaderboard.py (READ window aggregations to confirm coverage)</file>
    </files>
    <s3_writes>
      <write>s3://opal-data-bd/gold/canonical/nna_atomic/{YYYY-MM-DD}.parquet — bulk historical partitions (~2294)</write>
    </s3_writes>
  </scope>

  <wire_contract>
    Each historical partition file matches the schema of the daily 2026-04-13 partition (CN-P0 ratified 22-column list). No schema drift. Backfill is one-shot — does not change the daily CN-P1 writer.
  </wire_contract>

  <acceptance_criteria>
    1. Partition count ≥ legacy `gold/canonical/nna/` count.
    2. Each partition validates with `validate_nna_atomic.py --artifact {path}` invariants INV1/INV2/INV4/INV5 PASS.
    3. Spot-check parity: sum-by-date of canonical nna_atomic agrees with legacy nna for ≥90 sample dates within $0.01 OR divergence documented (atomic vs aggregate semantic difference).
    4. Rule 7 pre-flag MCP sent to CTO+COO BEFORE bulk S3 upload; 60-sec window observed.
    5. Session log Compiler Tools reproduces every `<run>` + observed + pass/fail vs `<expect>`.
    6. MCP COMPLETE to COO + CTO with: partition count, S3 prefix listing summary, validator summary, parity spot-check table covering all 9 D_00c window sizes.
    7. **AC ADDENDUM per CTO Path B clearance 2026-04-16 12:58Z:** per-date row-count AND per-date sum(inflows) + sum(outflows) comparison between backfilled `nna_atomic/{date}.parquet` and legacy C_03 cum columns (the pre-atomic source). Anchor: 2026-04-13 EXACT (±$0.00 on inflows+outflows; row count exact). Plus 3 RANDOM historical dates within ±1% on both sums (row count difference documented if non-exact — atomic vs legacy-cum semantic gap). Table emitted to session log + MCP COMPLETE body. This addendum is the gate that lets CN-P2 ship single-commit against validated backfill; missing = REWORK.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>aws s3 ls s3://opal-data-bd/gold/canonical/nna/ | wc -l &amp;&amp; aws s3 ls s3://opal-data-bd/gold/canonical/nna_atomic/ | wc -l</run>
        <expect>nna count ~2294, nna_atomic count = 1. Confirms backfill scope.</expect>
        <if_mismatch>If nna_atomic already &gt; 1, partial backfill exists — surface to COO.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-bd/gold/canonical/nna/ | head -3 &amp;&amp; aws s3 ls s3://opal-data-bd/gold/canonical/nna/ | tail -3</run>
        <expect>Earliest + latest dates visible (back to ~2018, latest ~2026-04-13).</expect>
        <if_mismatch>Window bounds unclear; investigate.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io C_01 &amp;&amp; comp-pipescript io D_00c</run>
        <expect>C_01 WRITES nna_atomic; D_00c READS the windows. Confirms producer + consumer.</expect>
        <if_mismatch>If D_00c reads from a different prefix, scope changes.</if_mismatch>
      </step>
      <step>
        <run>grep -nE 'window|3M|6M|1Y|2Y|3Y|MTD|QTD|YTD|MAX' data/black_diamond/scripts/gold/D_00c.advisor_leaderboard.py | head -20</run>
        <expect>9 window aggregations identified. Confirms required historical depth.</expect>
        <if_mismatch>If window list differs, document in TO.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile {backfill_script.py}</run>
        <expect>PY_COMPILE_OK.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>{backfill_script.py} --dry-run | wc -l</run>
        <expect>~2294 per-partition lines (matching legacy nna count).</expect>
        <if_mismatch>Re-tune window range.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="before S3 upload — RULE 7 PRE-FLAG MANDATORY">
      <step>
        <run>MCP send_message to 1.0.0_SA_CTO + 2.0.0_SA_COO subject "ACCEPTANCE FLEX / RULE 7 PRE-FLAG — CN-P1b bulk nna_atomic historical backfill (~2294 partitions)" body cites partition count + S3 prefix + 60-sec don't-object window</run>
        <expect>Pre-flag delivered. Wait 60 seconds. No CTO objection.</expect>
        <if_mismatch>HOLD upload, resolve.</if_mismatch>
      </step>
      <step>
        <run>{backfill_script.py} --upload</run>
        <expect>~2294 partitions uploaded; per-partition etag logged.</expect>
        <if_mismatch>Retry failed partitions.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-bd/gold/canonical/nna_atomic/ | wc -l</run>
        <expect>≥ legacy nna count.</expect>
        <if_mismatch>Investigate missing.</if_mismatch>
      </step>
    </phase>
    <phase id="4" when="after commit">
      <step>
        <run>for date in {90 sample dates}; do comp-validate canonical_nna_atomic --artifact gold/canonical/nna_atomic/${date}.parquet; done | grep -cE 'PASS'</run>
        <expect>90/90 PASS on INV1/INV2/INV4/INV5. comp-validate wrapper used so runs auto-log to `org/compiler-tools-log.md`.</expect>
        <if_mismatch>Document failures per date. Fall back to direct validate_nna_atomic.py only if comp-validate has missing schema pass-through.</if_mismatch>
      </step>
      <step>
        <run>For each of (2026-04-13 exact + 3 random historical dates): per-date row-count + sum(inflows) + sum(outflows) comparing nna_atomic/{date}.parquet to legacy C_03 cum_inflows/cum_outflows period-diff for same date.</run>
        <expect>2026-04-13: row-count exact + inflows/outflows ±$0.00. Random 3 dates: both sums within ±1% (row count documented if non-exact — atomic vs legacy-cum semantic gap). Table in session log. Satisfies AC #7 per CTO Path B clearance 2026-04-16 12:58Z.</expect>
        <if_mismatch>STOP. Do not MCP COMPLETE. Re-inspect backfill compute vs C_03 period-diff arithmetic. Surface to CTO+COO before retry.</if_mismatch>
      </step>
      <step>
        <run>For each D_00c window (3M/6M/1Y/2Y/3Y/MTD/QTD/YTD/MAX): sum nna_atomic partitions in that window vs sum legacy nna in same window for Travis Penfield. Output table.</run>
        <expect>9 window comparisons; deltas within $0.01 OR atomic-vs-aggregate semantic divergence documented per window.</expect>
        <if_mismatch>Investigate per-window divergence before MCP COMPLETE.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <!-- RE-SEQUENCED 2026-04-16 12:58Z per CTO Path B — CN-P1b is now the FIRST step in the ~D lane, no upstream deps. -->
    <dependency to="ADVI_ROLLUP.CN-P0" description="Canonical schema ratified (22-column list) — ships before backfill compute" status="complete" evidence="93b70620"/>
    <dependency to="ADVI_ROLLUP.CN-P1" description="Daily shadow writer exists and validated post-rerun" status="complete" evidence="bf9651b8 + 6c0da968 post-rerun validators PASS"/>
  </dependencies>

  <next>
    CN-P1b close → unblocks CN-P3 (~B) re-fire → unblocks CN-P4 (~B D_01 partner_analytics cutover) → unblocks Wave 4 convergence gate.
  </next>
</task_order>
