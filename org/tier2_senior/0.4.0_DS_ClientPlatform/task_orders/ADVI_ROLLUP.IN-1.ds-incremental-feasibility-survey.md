<task_order>
  <metadata>
    <id>ADVI_ROLLUP.IN-1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to><!-- base lane -->
    <date>2026-04-15</date>
    <status>complete</status><!-- Closed 2026-04-15 PM. 11 ELIGIBLE / 12 CONDITIONAL / 4 INELIGIBLE. Top-3: D_02, A_03, B_01. Memo + JSON at docs/analysis/2026-04-15_incremental_runs_feasibility.{md,json}. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>IN (Incremental runs — Wave 7)</wave>
    <priority>P1 (foundational survey; gates IN-2 design + IN-3+ implementation)</priority>
  </metadata>

  <references>
    <ref type="trigger">Andrew 2026-04-15 PM: "figure out if it's possible to make true incremental runs rather than every table being a full run every time"</ref>
    <ref type="related">data/black_diamond/scripts/gold/ — all gold-layer scripts in scope for the survey</ref>
    <ref type="related">data/black_diamond/scripts/runner/gold_dispatch.sh `--incremental` flag (currently restricted to A_00 + C_06 per ADVI_ROLLUP.DH-2)</ref>
  </references>

  <objective>
    Survey every gold-layer script (S_*, A_*, B_*, C_*, D_*) for true-incremental feasibility. Today every table is rebuilt from scratch every nightly fire; some scripts genuinely need the full rebuild (graph closures, cumulative aggregations across history) but many are append-friendly (date-partitioned, idempotent-by-key). Identify which scripts CAN go incremental and what each one needs.

    **Deliverable: per-script feasibility memo** at `docs/analysis/2026-04-15_incremental_runs_feasibility.md` containing:

    1. **Per-script row**, columns:
       - script id (e.g. `B_01`)
       - current run mode (full-rebuild / append-only / mixed)
       - output partition scheme (date-keyed / unpartitioned / advisor-keyed / etc)
       - watermark feasibility (does the script have a natural watermark? candidate columns?)
       - idempotent-merge feasibility (can a re-run on overlapping window produce identical output?)
       - dependencies that block incremental (e.g. cumulative aggregations, cross-date joins, lookbacks)
       - **verdict:** ELIGIBLE / INELIGIBLE / CONDITIONAL — with one-sentence reason
       - if ELIGIBLE: rough effort estimate (S/M/L)

    2. **Cross-script dependency map** — even if a script is locally eligible, downstream consumers may break if upstream goes incremental (e.g. `D_02` reads many `C_*` outputs; if any upstream is "yesterday only" while D_02 expects "all-history," D_02 silently breaks). Identify the "incremental wave" cuts: groups of scripts that must transition together.

    3. **Recommended priority ordering** — which scripts to convert first for max efficiency gain with minimum risk. Wall-time + CPU+RAM cost per script (use AE's recent rerun walltimes from `org/tier2_senior/0.6.0_AE_PartnerETL/logs/2026-04-15/full_chain_recovery_b01_namerror_fix.md` as the baseline; cite the table).

    4. **Cross-cutting concerns** to flag for IN-2 design phase (CTO PRD candidates):
       - watermark column convention (is there a single column name we adopt across all gold? e.g. `_ingest_ts`, `_partition_date`)
       - merge strategy (parquet partition overwrite vs delta-append vs custom)
       - re-run validation (how do we prove an incremental run produced same output as a full rebuild?)
       - rollback / disaster recovery (what's the path back to full-rebuild if an incremental run silently corrupts?)

    Survey is READ-ONLY. No code changes in this TO. Output is the memo + a structured JSON sidecar (`docs/analysis/2026-04-15_incremental_runs_feasibility.json`) for downstream comp-tooling.
  </objective>

  <scope>
    <files>
      <file action="create">docs/analysis/2026-04-15_incremental_runs_feasibility.md</file>
      <file action="create">docs/analysis/2026-04-15_incremental_runs_feasibility.json</file>
      <file action="reference_only">data/black_diamond/scripts/gold/**/*.py</file>
      <file action="reference_only">data/black_diamond/scripts/runner/gold_dispatch.sh</file>
    </files>
  </scope>

  <acceptance_criteria>
    1. Memo + JSON sidecar exist at the paths above.
    2. Every script under `data/black_diamond/scripts/gold/` (S_*, A_*, B_*, C_*, D_*) is listed in the per-script table — none skipped.
    3. Cross-script dependency map cites comp-pipescript io/feeds/consumers output for at least the highest-cost scripts (D_02, B_01, C_06).
    4. Priority ordering cites AE's wall-time table; recommended top-3 ELIGIBLE scripts have clear effort + risk reasoning.
    5. Cross-cutting concerns section lists at least 4 distinct IN-2 design questions for CTO PRD.
    6. Session log Compiler Tools reproduces every `<run>` + observed + pass/fail.
    7. MCP COMPLETE to COO with memo path + JSON path + top-3 priority recommendation.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>ls data/black_diamond/scripts/gold/ | grep -E '^[A-Z]_[0-9].*\.py$' | sort</run>
        <expect>Full enumeration of gold scripts. This is the table population list.</expect>
        <if_mismatch>If any script is missing or path differs, baseline against actual repo state.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io D_02 &amp;&amp; comp-pipescript io B_01 &amp;&amp; comp-pipescript io C_06</run>
        <expect>I/O graph for the three highest-cost scripts. READS list informs upstream-dep map; WRITES list informs partition scheme.</expect>
        <if_mismatch>If comp-pipescript fails on any of these, surface to COO — comp-tools cache may need rebuild.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript feeds D_02</run>
        <expect>Upstream dependency tree for D_02. Confirms which C_* outputs must move together if D_02 goes incremental.</expect>
        <if_mismatch>Document in memo.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>jq -r '.scripts[].id' docs/analysis/2026-04-15_incremental_runs_feasibility.json | sort &gt; /tmp/in1_json_ids.txt &amp;&amp; ls data/black_diamond/scripts/gold/ | grep -E '^[A-Z]_[0-9].*\.py$' | sed 's/\.py$//' | sort &gt; /tmp/in1_disk_ids.txt &amp;&amp; diff /tmp/in1_json_ids.txt /tmp/in1_disk_ids.txt</run>
        <expect>Empty diff (every disk script appears in JSON, no extras).</expect>
        <if_mismatch>Add missing script rows or remove stale entries.</if_mismatch>
      </step>
      <step>
        <run>jq '[.scripts[] | select(.verdict == "ELIGIBLE")] | length' docs/analysis/2026-04-15_incremental_runs_feasibility.json</run>
        <expect>Non-zero (at least some scripts identified as ELIGIBLE — this is the whole point of the survey).</expect>
        <if_mismatch>If zero ELIGIBLE, IN-2 design phase is moot. Re-examine survey rigor before declaring done.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>git log --oneline -1 -- docs/analysis/2026-04-15_incremental_runs_feasibility.md</run>
        <expect>Commit visible with author=base DS lane.</expect>
        <if_mismatch>Re-commit with correct author.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency to="ADVI_ROLLUP.SL-P0" description="Base DS finishes SL-P0 sleeve discovery first (single-lane on base)" status="pending"/>
  </dependencies>

  <next>
    IN-1 close gates IN-2 (design PRD authoring — likely bounces to CTO for blessing) which gates IN-3+ (per-script implementation TOs, dispatched after IN-2 lands).
  </next>
</task_order>
