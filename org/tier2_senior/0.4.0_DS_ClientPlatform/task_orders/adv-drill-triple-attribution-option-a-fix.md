<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-adv-drill-triple-attribution-option-a</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. --><!-- HELD 2026-04-14T23:20Z — CTO scope revision after initial GO. DS commit on CLOUD reflects prior scope ($391.66M target via rel_architect_lookup); revised target is $390.37M via account-level attribution mirroring D_00c. DS must revise + keep local; NO S3 upload until post-presentation + Andrew GO. -->
    <project_code>ad-hoc</project_code>
    <priority>post-presentation — Andrew GO required</priority>
  </metadata>

  <references>
    <ref type="analysis">docs/analysis/2026-04-14_travis_penfield_adv_aua_triple_attribution_bug.md</ref>
    <ref type="directive">Andrew 2026-04-14 — Option A approved; stage, do not fire until post-presentation</ref>
  </references>

  <objective>
    **REVISED 2026-04-14T23:18Z per CTO — target is $390.37M canonical (Leaderboard), NOT $391.66M.**
    The original rel_architect_lookup approach is relationship-level and would leave L0+L1 drill
    $1.29M off canonical.

    In `data/black_diamond/scripts/gold/D_00b.portal_timeseries.py`, rebuild the architect slice
    of BOTH the L0 aggregate (lines 721-729, currently reads `nna_aua_by_advisor.parquet`) AND
    the L1 drill (lines 806-822) using ACCOUNT-LEVEL attribution: filter `account_performance`
    joined to `account_team` where `account_team.architect == arch` — exactly the same rule as
    `D_00c.portal_leaderboard.py`. Consistency of rule is more important than elegance.

    - Ignore `nna_aua_by_advisor.parquet`'s architect slice for this chart.
    - Ignore `cdim.primary_architect` as a filtering source.
    - Keep `cdim.primary_architect` as a dimension display column (no semantics change).

    Effectively scoped-down Option B — account-level inline without upstream parquet rebuild.
    Full upstream rebuild stays as candidate BDPL_CNPRCS WP-10 (not authored).
  </objective>

  <scope>
    <file>data/black_diamond/scripts/gold/D_00b.portal_timeseries.py</file>
    <change>
      Two blocks touched in the same file (both architect-slice paths):

      1. L0 aggregate (lines 721-729) — currently reads `nna_aua_by_advisor.parquet`.
         Replace with account-level join: filter account_performance by
         account_team.architect == arch (same rule D_00c.portal_leaderboard.py uses).

      2. L1 drill (lines 806-822) — currently filters perf_cohort['primary_architect'] == arch.
         Replace with the same account-level join.

      DS reads D_00c.portal_leaderboard.py FIRST to mirror its exact filter logic.
      No new columns, no schema change — only swap the filter source on two blocks.
    </change>
  </scope>

  <acceptance_criteria>
    1. **Internal consistency:** `abs(sum(adv_drill[X].data[-1]) - adv.data[-1][X]) < $1.0` for every architect X
    2. **Canonical consistency:** `abs(adv.data[-1][X] - Leaderboard.employee_leaderboard.windows[*].entries[i].role_breakdown.architect.aua) < $1.0` for every architect where both surfaces emit X
    3. **Travis spot-check:** `adv.data[-1]['Travis Penfield']` = $390.37M ± $1 AND `adv_drill['Travis Penfield']` top-9 + Other sums to $390.37M ± $1
    4. Firm-wide disagreement census in session log (as before — per-architect rel-count diff rel_architect_lookup vs cdim.primary_architect — useful for post-fix diagnostics)
    5. Zero change to other consumers — geo drill, cla_adv_drill at :844, and any other `primary_architect` consumer untouched. Only the two architect-slice blocks (721-729 + 806-822) are modified
    6. MCP COMPLETE to COO with commit + firm-wide census + Travis spot-check + Leaderboard tie-out snippet for 3 sample architects (not just Travis)
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io D_00b.portal_timeseries.py`; **`comp-pipescript io D_00c.portal_leaderboard.py`** (read the exact account-level filter rule and mirror it in D_00b — consistency of rule > elegance, per CTO 2026-04-14T23:18Z); `comp-pipescript consumers cumulative_chart.json`.
    Phase 2: `python -m py_compile D_00b.portal_timeseries.py`; `comp-validate D_00b` after gold rerun.
    Phase 3: `comp-transform schema-check DistributionTab --feature advDrill` — confirm no FE side impact.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    NONE. `D_00b.adv_drill` is a single-writer/single-reader artifact per DS's analysis. Other drills (geo, cla_adv) in the same script are NOT touched.
  </cross_domain_coordination>

  <out_of_scope>
    - No change to Leaderboard / AdvisorPublicProfile math.
    - No change to nna_adv_drill (D_04:1908-1931) — separate audit if Andrew wants NNA verified.
    - No change to cdim.primary_architect semantics (it stays as a dimension column).
    - NO Option B work (account-grain attribution, cdim.primary_architect filtering drop) — candidate BDPL_CNPRCS WP-10 later, NOT in this TO. Andrew: "Option A for now."
  </out_of_scope>

  <dependencies>
    <none/>
  </dependencies>
</task_order>
