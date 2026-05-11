<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.A-GROUP-AUDIT</id>
    <project>ADVI_INFNNA</project>
    <title>INF gold A-layer (A_00–A_04) efficiency + reality audit — investigate whether A-scripts are dialed into current data shape; identify redundant compute, deprecated paths, missing parallelization</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>pending</status>
    <priority>medium</priority>
    <estimated_effort>~3-5h (read + audit + document; no script rewrites in this TO)</estimated_effort>
    <authorized_by>Andrew direct 2026-05-11 ("A Group of gold runner scripts may not actually be dialed into the reality of the data... could be failing and taking unnecessary time/compute")</authorized_by>
  </metadata>

  <references>
    <ref type="parent_observation">Andrew 2026-05-11: A-group scripts may be doing unnecessary work; INF_A_03.positions_cube ran 9.7min wall + 3,362MB peak mem + 690% CPU on Friday's instrumented cascade — heaviest single A-script.</ref>
    <ref type="friday_telemetry">.runtmp/telemetry/2026-05-08/inf-gold-layer-runner/ — full per-second CPU/Mem/IO/Threads for each A-script across instrumented cascade `cascade-192259Z-245079b1.log`</ref>
    <ref type="todays_telemetry">.runtmp/telemetry/2026-05-11/inf-gold-layer-runner/ — re-cascade with widened coerce_id_columns; provides second data point</ref>
    <ref type="affected_scripts">data/orion/scripts/gold/INF_A_00.accounts_dimension.py, INF_A_01.advisor_assignments.py, INF_A_02.fee_rate_history.py, INF_A_03.positions_cube.py, INF_A_04.client_dimension.py</ref>
  </references>

  <context>
    The INF gold A-layer is foundational — A-scripts produce dimensional tables that B/C/D-layer scripts consume. If A-scripts are inefficient or do work they don't need, the cost cascades through the rest of the pipeline.

    **Andrew's hypothesis:** A-scripts may not be dialed into the actual current data shape — they may be:
    - Reading deprecated columns / dim paths that no longer exist or have shifted
    - Doing unnecessary joins across dims (e.g., re-reading unified_account_dim when accounts_v2 already has the columns)
    - Missing parallelization opportunities (Friday cascade showed C_03 hit 828% CPU / 279 threads but A-scripts were mostly single-threaded)
    - Processing redundant data (e.g., positions_cube reading 6 years of positions when only the snapshot date matters)
    - Carrying ETL-stale logic from pre-INFNNA / pre-CANNNA architecture

    **Friday baseline (heaviest A-scripts):**
    - INF_A_03.positions_cube: 9.7 min wall / 3,362 MB peak mem / 690% CPU / 14 threads
    - INF_A_00.accounts_dimension: ~30s wall (fast but FAILS on dtype drift — see ACCOUNT-ID-COERCE)
    - INF_A_01.advisor_assignments: ~30s wall (fast but FAILED Friday on dtype drift)
    - INF_A_04.client_dimension: ~30s wall

    A_03 is the lead suspect — 9.7min is 14% of total cascade wall-clock.

    **Scope intent:** read + audit + document. NO script rewrites in this TO. If efficiency wins are found, surface in RAVC and we'll author a follow-up TO with the actual changes (could go to DS~B as continuation or DS~A as architecture owner).
  </context>

  <scope>
    <step>
      **Read every A-script source.** Build a mental + written model of each:
      - Input dims read (from silver/, bronze/, S3 paths)
      - Logical transformations (joins, filters, aggregations)
      - Output columns written
      - Parallelization usage (multiprocessing, threading, polars vs pandas)
      - Any TODO comments, stale docstrings, or "temporary" code that's still there

      Output: per-script summary in session log.
    </step>

    <step>
      **Cross-reference Friday + today telemetry.** Read `.runtmp/telemetry/2026-05-08/` AND `.runtmp/telemetry/2026-05-11/` for each A-script. Compute:
      - Mean CPU, peak CPU, mean memory, peak memory, wall-clock
      - IO read MB, IO write MB
      - Thread count (parallelism witness)

      Identify mismatches between actual resource shape and what the script "should" be doing.
    </step>

    <step>
      **Audit each script against current data reality:**

      **(a) Path validity:** for every S3 read/write path in script source, verify the path exists with current data via `aws s3 ls`. Flag any deprecated/missing paths.

      **(b) Column validity:** for every column the script reads from a silver dim, verify that column exists in current silver partitions (sample 3 dates). Flag stale column references.

      **(c) Join necessity:** for every merge/join, determine if the join is necessary. Common anti-patterns:
      - Re-reading a dim that's already merged upstream
      - Joining on a column that always has 1:1 mapping (could be eliminated)
      - Reading full historical when only snapshot date is needed

      **(d) Filter timing:** filters applied AFTER expensive joins waste compute. Flag any filter-after-expensive-op patterns.

      **(e) Parallelization opportunity:** Friday showed C_03 hit 828% CPU naturally. Are A-scripts missing parallelization wins they could trivially adopt?
    </step>

    <step>
      **Specific INF_A_03 deep-dive (lead suspect).** It's 14% of cascade wall-clock and 3.3GB peak memory. Determine:
      - Why 3.3GB peak? What's the largest dataframe in memory at peak?
      - Could the per-date positions read be parallelized (it's bottlenecked by per-date sequential)?
      - Is positions_cube reading ALL historical positions when only certain dates are needed downstream?
      - Could polars replace pandas for the heavy data-frame ops?

      Output: hypothesis + suggested experiment for follow-up TO.
    </step>

    <step>
      **Compare A-script architecture to BD/49F equivalents.** Inflection's A-scripts may be a port of BD/49F patterns. Read the equivalent BD/49F scripts (likely `data/black_diamond/scripts/gold/A_*` or similar). Note:
      - Architectural divergences
      - Which version is "newer" / more efficient
      - Inflection-specific simplifications that should have happened but didn't (e.g., Inflection has 4 advisors vs 49F's 150 — should A-scripts be doing per-advisor work that 4-advisor case doesn't need?)
    </step>

    <step>
      **Output: findings document + recommendations.** Path: `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-11/DS_B_a_group_audit_findings.md`.

      Structure:
      - Per-script summary (purpose, input, output, current cost)
      - Per-script audit findings (a-e above)
      - INF_A_03 deep-dive section
      - BD/49F architectural comparison
      - Recommended efficiency wins, prioritized by (estimated wall-clock savings × confidence)
      - Suggested follow-up TOs (concrete + scoped)
    </step>

    <step>
      **RAVC to COO.** Surface top 3 findings + top 3 recommended follow-up TOs. Include estimated wall-clock savings if recommendations land.
    </step>
  </scope>

  <acceptance_criteria>
    1. **Per-script summary** for all 5 A-scripts in session log.
    2. **Telemetry cross-reference** (Friday + today) completed; resource shape observations documented.
    3. **Audit findings** for each script across (a) path validity, (b) column validity, (c) join necessity, (d) filter timing, (e) parallelization opportunity.
    4. **INF_A_03 deep-dive** with at minimum 1 testable hypothesis for efficiency improvement.
    5. **BD/49F comparison** with at least 3 architectural divergences noted.
    6. **Findings document** at canonical path; cleanly structured.
    7. **Top-3 follow-up TO recommendations** with effort estimates + expected savings.
    8. **RAVC delivered** with executive summary + top findings.
  </acceptance_criteria>

  <blocking>
    No upstream gates. Independent investigation; can run in parallel with ACCOUNT-ID-COERCE cascade + LEADERBOARD-JOE-ABSENT.

    Do NOT modify any A-script source in this TO — read-only audit. Modifications happen in follow-up TOs after findings are reviewed.
  </blocking>

  <notes>
    **DS~B onboarding context (2026-05-11):** Andrew brought DS~B online specifically to expand capacity and parallel investigation. This is your first TO on this project. DS~A is heads-down on cascade-related work; you have orthogonal scope (efficiency audit) so you don't step on their lane.

    **Read-only intent is critical** — the goal is to BUILD a model of A-layer reality before touching it. Premature optimization = the root of many drifts. Audit first, propose changes second.

    **If you find an outright bug** (not just inefficiency), surface immediately via RAVC; don't wait for the audit document. Same protocol as any data-correctness incident.

    **Telemetry baseline already exists** — use `runner-telemetry-analyze.py` (DS~A's tool, `.tools/`) for distribution stats across both Friday + today cascades.
  </notes>
</task_order>
