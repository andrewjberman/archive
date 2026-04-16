<task_order>
  <metadata>
    <id>ADVI_ROLLUP.RA-P1b</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- staged→pending 2026-04-16 by 2.0.0_SA_COO. CN-P1b COMPLETE dc4980c3, CN-P2 COMPLETE ebd737e3 — hard gate cleared. GO dispatched to DS~D 20260416T163557Z. COMPLETE 2026-04-16 by 0.4.0_DS_ClientPlatform~D. Commit c962ddb3 on CLOUD: C_01b.role_aua_backfill.py created; 2,293 new partitions uploaded (2,294 total in S3), 390,974 rows. Parity spot-check 28/30 PASS (2 SKIP early $0-AUA dates), 0 FAIL, diff_pct=0.000% on all non-zero dates. Account_performance source; account_team current-snapshot role assignments retroactively applied. Schema matches _ROLE_AUA_COLS. RA-P2b unblocked. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>4 (Structural convergence)</wave>
    <priority>P1 (gates RA-P2b D_02 timeseries cutover + Wave 4 convergence gate)</priority>
  </metadata>

  <references>
    <ref type="trigger">CTO redline 2026-04-15 21:39Z + 21:48Z — RA-P1 latest-date-only shadow writer leaves single partition; D_02 L1632-1655 timeseries consumer needs multi-date coverage</ref>
    <ref type="prereq">ADVI_ROLLUP.RA-P1 — daily shadow writer (commit 6c0da968)</ref>
    <ref type="related">ADVI_ROLLUP.RA-P2 — snapshot-only cutover (commit 0c06d423)</ref>
    <ref type="related">ADVI_ROLLUP.RA-P2b — D_02 timeseries cutover, hard-gates on this TO</ref>
    <ref type="prd">docs/architecture/ROLE_AUA_CANONICAL_CONVERGENCE_PLAN.md</ref>
  </references>

  <objective>
    Backfill `gold/canonical/role_aua/{YYYY-MM-DD}.parquet` for the historical window required by D_02 timeseries consumer (L1619-1632 build_advisor_timeseries.role_ts_lookup). Same compute path as the CN-P1 daily writer; bulk-loop over historical dates from silver/allocations.

    **Window decision (CTO direction):** READ the consumer first. Open D_02 L1619-1632 in `data/black_diamond/scripts/gold/D_02.advisor_client_detail.py` and document in this TO's opening section the exact date range L1619-1632 iterates. Backfill exactly that range. If the range is parameterized/dynamic, default to silver allocations earliest available date (cheap to over-backfill, expensive to under-backfill).

    **Source:** silver inflows/outflows + allocations historical. Same compute path as CN-P1 daily writer (you authored — reuse the function). Per-date loop, partition-write to S3.

    **Validator:** partition count must be ≥ what the consumer iterates over. Spot-check sum-by-date parity against legacy role_aua source (whatever D_02 currently reads pre-cutover) for ≥30 dates. Document divergence.

    **CRITICAL — Rule 7 pre-flag MANDATORY before `aws s3 cp` / `--upload`** for the bulk historical write. This is A→D-rerun-sensitive surface (you wrote `feedback_ad_rerun_sensitive_preflag_before_s3_write.md` — apply your own rule). Send 1-line MCP to CTO+COO BEFORE the upload, 60-sec don't-object window.
  </objective>

  <scope>
    <files>
      <file action="create_or_extend">data/black_diamond/scripts/gold/C_01.role_aua.py (extend with --historical-backfill mode, OR write a separate one-off backfill script alongside)</file>
      <file action="reference_only">data/black_diamond/scripts/gold/D_02.advisor_client_detail.py (READ L1619-1632 for window spec)</file>
    </files>
    <s3_writes>
      <write>s3://opal-data-bd/gold/canonical/role_aua/{YYYY-MM-DD}.parquet — bulk historical partitions</write>
    </s3_writes>
  </scope>

  <wire_contract>
    Each historical partition file matches the schema of the daily 2026-04-13 partition (RA-P0 ratified column list). No schema drift. Backfill is one-shot — does not change the daily CN-P1 writer.
  </wire_contract>

  <acceptance_criteria>
    1. Window range documented in this TO's `<objective>` opening section before code is written, citing D_02 line refs and date math.
    2. Backfill produces N partitions where N ≥ consumer-required window count.
    3. Each partition validates with `validate_role_aua.py --artifact {path}` invariants I1/I2/I5/I6 PASS.
    4. Spot-check parity: sum-by-date of canonical role_aua agrees with legacy D_02 pre-cutover read for ≥30 sample dates within $0.01 per date or documented divergence reason.
    5. Rule 7 pre-flag MCP sent to CTO+COO BEFORE bulk S3 upload; 60-sec window observed.
    6. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail vs `<expect>` (CTO Rule 7).
    7. MCP COMPLETE to COO + CTO with: partition count, S3 prefix listing summary, validator summary, parity spot-check table.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>sed -n '1610,1660p' data/black_diamond/scripts/gold/D_02.advisor_client_detail.py</run>
        <expect>build_advisor_timeseries.role_ts_lookup logic visible at L1619-1632; date iteration range identifiable.</expect>
        <if_mismatch>Lines may have shifted post-RA-P2 commit (0c06d423). Re-locate via `grep -n role_ts_lookup` and update window-spec section.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-bd/gold/canonical/role_aua/ | wc -l</run>
        <expect>1 (only 2026-04-13.parquet from RA-P1).</expect>
        <if_mismatch>If &gt; 1, partial backfill exists — surface to COO before adding more.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io C_01</run>
        <expect>WRITES includes `gold/canonical/role_aua/` + `gold/canonical/nna_atomic/` (CN-P1 emit). Confirms reuse path.</expect>
        <if_mismatch>If C_01 doesn't emit role_aua, the writer lives elsewhere; locate before writing backfill.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-bd/silver/allocations/ | head -5 &amp;&amp; aws s3 ls s3://opal-data-bd/silver/allocations/ | tail -5</run>
        <expect>Silver allocations earliest + latest dates visible. Bounds the backfill window.</expect>
        <if_mismatch>If silver/allocations missing, escalate to AE — backfill source unavailable.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile {backfill_script.py}</run>
        <expect>PY_COMPILE_OK.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>{backfill_script.py} --dry-run | head -50</run>
        <expect>Per-date iteration plan visible; partition count matches window spec.</expect>
        <if_mismatch>Re-tune window range.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="before S3 upload — RULE 7 PRE-FLAG MANDATORY">
      <step>
        <run>MCP send_message to 1.0.0_SA_CTO + 2.0.0_SA_COO subject "ACCEPTANCE FLEX / RULE 7 PRE-FLAG — RA-P1b bulk historical backfill upload" body cites partition count + S3 prefix + 60-sec don't-object window</run>
        <expect>Pre-flag delivered. Wait 60 seconds. No CTO objection received.</expect>
        <if_mismatch>If CTO objects, HOLD upload and resolve.</if_mismatch>
      </step>
      <step>
        <run>{backfill_script.py} --upload</run>
        <expect>Upload success; per-partition etag logged.</expect>
        <if_mismatch>Retry per-partition; surface persistent failures.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-bd/gold/canonical/role_aua/ | wc -l</run>
        <expect>Count matches expected post-backfill (initial 1 + N new partitions).</expect>
        <if_mismatch>Investigate missing partitions.</if_mismatch>
      </step>
    </phase>
    <phase id="4" when="after commit">
      <step>
        <run>for date in {30 sample dates}; do validate_role_aua.py --artifact gold/canonical/role_aua/${date}.parquet; done | grep -E 'PASS|FAIL'</run>
        <expect>30/30 PASS on I1/I2/I5/I6.</expect>
        <if_mismatch>Document failures; may require partial re-backfill.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency to="ADVI_ROLLUP.CN-P1b" description="~D lane sequencing per CTO Path B 2026-04-16 12:58Z: CN-P1b backfill ships FIRST; RA-P1b interleaves/follows on same ~D lane. (Prior dep on CN-P2 was the pre-re-sequence plan.)" status="complete" evidence="dc4980c3"/>
  </dependencies>

  <next>
    RA-P1b close → unblocks RA-P2b dispatch (~C).
  </next>
</task_order>
