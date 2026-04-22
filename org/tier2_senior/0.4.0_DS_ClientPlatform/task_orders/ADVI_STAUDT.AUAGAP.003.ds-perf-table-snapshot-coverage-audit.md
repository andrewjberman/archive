<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-22-auagap-003-perf-audit</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-22</date>
    <status>complete</status><!-- Closed 2026-04-22 — subsumed by full RCA finalization (43c7e5db / bb823bf8 / 214430d8). Snapshot coverage finding integrated into the composite root cause document at data/black_diamond/diagnostics/aua25q_rca.md. Status drift flip per COO reconciliation. -->
    <project_code>ADVI_STAUDT</project_code>
    <urgency>URGENT — run in parallel with AUAGAP.001 + .002. Andrew watching.</urgency>
  </metadata>

  <objective>
    Inventory perf table snapshot dates for 2024-12 through 2026-01. Test Hypothesis C:
    D_00b _snap_date picks closest perf date ≤ period_end, but if perf is sparse in
    Q1-Q3 2025, the snap lands on a partial/early-month date with understated AUA.
    Output: data/black_diamond/diagnostics/aua25q_perf_bisect.md
  </objective>

  <context>
    D_00b.portal_timeseries.py _build_static_aua_periods uses _snap_date to pick closest
    perf date ≤ quarter period_end. If the perf table has dates 2024-12-31 and 2025-12-31
    but sparse or missing dates in between, Q1/Q2/Q3 2025 quarter snapshots could be
    snapping to early-January or month-start dates before settlement — producing partial
    (understated) AUA rather than end-of-period settled AUA.

    Source: wherever client_performance lives (silver/client_performance/ or gold/perf/).
    DO NOT attempt fixes. Diagnostic only.
  </context>

  <spec>
    Source: perf table (silver/client_performance/ or gold/timeseries/perf/ — check both)
    Date range: 2024-12-01 through 2026-01-31

    Analysis:
    1. Inventory: list all distinct snapshot dates present in perf for this range.
    2. Per date: count(distinct relationship_id), sum(total_aua), count(rows).
    3. Identify: are there sparse gaps in 2025 Q1-Q3? Expected: ~daily or monthly entries.
       If only month-start dates exist for Q1-Q3 2025, _snap_date picks those over month-end.
    4. Key test: for 2025-03-31, 2025-06-30, 2025-09-30 — what is the closest perf date ≤
       that date? What is sum(total_aua) on that date vs 2024-12-31 baseline?
    5. If those snap dates fall on month-start (2025-01-02, 2025-04-01, etc.) rather than
       month-end → HYP C confirmed. The chart isn't wrong; it's showing early-month data.

    Output: data/black_diamond/diagnostics/aua25q_perf_bisect.md
    Content:
    - Full inventory of distinct perf dates in range (list them)
    - Table: (quarter_end, nearest_snap_date, snap_type[month-start/month-end/mid-month],
      sum_total_aua, rel_count, delta_vs_q42024)
    - Summary: HYP C CONFIRMED / HYP C NOT ROOT CAUSE with the snap dates as evidence.
  </spec>

  <acceptance_criteria>
    1. Full perf date inventory for 2024-12-01 through 2026-01-31 produced.
    2. Per-date: rel_count + sum_total_aua + row_count reported.
    3. Quarter-end snap dates for Q1/Q2/Q3 2025 explicitly identified.
    4. Snap type classified: month-start vs month-end vs mid-month.
    5. Output committed: data/black_diamond/diagnostics/aua25q_perf_bisect.md.
    6. MCP CTO + COO with HYP C verdict.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT attempt fixes. Diagnostic only.</rule>
    <rule>Do NOT run pipeline scripts — S3 query only.</rule>
    <rule>Do NOT wait for AUAGAP.001 or .002 before reporting if snap-date gap is definitive.</rule>
  </do_not>
</task_order>
