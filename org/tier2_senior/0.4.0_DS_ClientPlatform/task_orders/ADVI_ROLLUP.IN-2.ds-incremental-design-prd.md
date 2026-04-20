<task_order>
  <metadata>
    <id>ADVI_ROLLUP.IN-2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to><!-- base lane; may bounce to CTO for PRD authoring -->
    <date>2026-04-15</date>
    <status>complete</status><!-- 2026-04-16: scope-absorbed by CTO per ABSORB CONFIRMED 14:00Z. PRD at docs/architecture/INCREMENTAL_RUNS_DESIGN.md committed 916a3a4f (CTO author). PRD covers all 7 scope items across 13 sections (watermark contract §3, merge strategy §4, parity validator §5, hard gates §6, wave plan §7, cross-domain coordination §8, telemetry/risk §10/11). Closure note: scope-absorbed by CTO, not DS-authored delivery. IN-3+ per-script implementation TOs author against PRD §Acceptance + §Compiler mandates. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>IN (Incremental runs — Wave 7)</wave>
    <priority>P1 (gates IN-3+ implementation)</priority>
  </metadata>

  <references>
    <ref type="trigger">Andrew 2026-04-15 PM: "true incremental runs rather than every table being a full run every time"</ref>
    <ref type="prereq">ADVI_ROLLUP.IN-1 — feasibility survey memo + JSON</ref>
    <ref type="related_design">CTO may absorb this TO and author as a PRD instead — see "potential bounce" in `<objective>`</ref>
  </references>

  <objective>
    Given IN-1's per-script feasibility verdict, design the canonical incremental-run contract that all ELIGIBLE scripts adopt. This is the design lock that IN-3+ implementation TOs reference.

    **Deliverable: design doc** at `docs/architecture/INCREMENTAL_RUNS_DESIGN.md` covering:

    1. **Canonical watermark contract** — single column name + dtype convention (e.g. `_partition_date date`, or `_ingest_ts timestamp`). Every ELIGIBLE script writes this column. Define handling for backfill / replay / late-arriving data.
    2. **Merge strategy** — parquet partition overwrite vs delta-append vs hive-style. Per-script override possible? Default?
    3. **Re-run validation contract** — how does each ELIGIBLE script prove an incremental run produces the same output as a full rebuild on the same window? (e.g. weekly full-rebuild + diff against running incremental result; row-count checksums; spot-check tooling.)
    4. **Dispatcher contract** — what does `--incremental` mean across the full chain? Per-script flag? Per-chain flag? Watermark resolution: dispatcher computes the window or each script computes its own?
    5. **Rollback / disaster recovery** — if an incremental run silently corrupts, what's the path back to a clean full-rebuild? S3 versioning? Snapshot artifacts? Re-runnable from when?
    6. **Cross-script wave cuts** — based on IN-1's dependency map, the staged transition order. Which scripts move together? Which standalone?
    7. **Telemetry + alerting** — every incremental run emits row-count delta + watermark advanced + duration; FAIL alert on stalled watermark, row-count regression, etc.

    **Potential bounce:** if the design surface is broader than DS scope (touches dispatcher contract, S3 layout, alerting infra), CTO may absorb this and author as a PRD. Base DS authors v0.1 draft; if CTO wants to take over, hand off cleanly with the v0.1 as starting point.
  </objective>

  <scope>
    <files>
      <file action="create">docs/architecture/INCREMENTAL_RUNS_DESIGN.md</file>
    </files>
  </scope>

  <acceptance_criteria>
    1. Design doc exists with all 7 sections populated.
    2. Each section cites IN-1 evidence (per-script memo rows).
    3. Doc identifies a "Wave 1" set of 2-4 scripts that can convert with lowest risk + highest reward, with effort estimate.
    4. Doc identifies the "INELIGIBLE-permanent" scripts that will always run full and explains why.
    5. CTO has reviewed and either (a) blessed the design, or (b) absorbed authorship and produced a v1.0 PRD.
    6. Session log Compiler Tools reproduces every `<run>` + observed + pass/fail.
    7. MCP COMPLETE to COO + CTO with design doc path and CTO disposition.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>cat docs/analysis/2026-04-15_incremental_runs_feasibility.md | head -100</run>
        <expect>IN-1 memo readable; per-script verdicts visible.</expect>
        <if_mismatch>IN-1 not closed — STOP. Wait for IN-1 GO.</if_mismatch>
      </step>
      <step>
        <run>jq '[.scripts[] | select(.verdict == "ELIGIBLE") | .id]' docs/analysis/2026-04-15_incremental_runs_feasibility.json</run>
        <expect>List of ELIGIBLE script ids — informs the Wave 1 set selection.</expect>
        <if_mismatch>If empty, design moot — surface to COO + CTO.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>grep -cE '^## ' docs/architecture/INCREMENTAL_RUNS_DESIGN.md</run>
        <expect>Count &gt;= 7 (all required sections present).</expect>
        <if_mismatch>Add missing sections.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>MCP send_message to 1.0.0_SA_CTO with design doc path</run>
        <expect>CTO ACK with disposition (bless / absorb / redline).</expect>
        <if_mismatch>If no CTO response within 30 min, MCP COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency to="ADVI_ROLLUP.IN-1" description="Per-script feasibility survey complete" status="complete" evidence="196e8e53"/>
  </dependencies>

  <next>
    IN-2 close (with CTO blessing) gates IN-3+ — per-script implementation TOs. Likely 5-10 TOs to convert the Wave 1 ELIGIBLE set, dispatched after IN-2 lands.
  </next>
</task_order>
