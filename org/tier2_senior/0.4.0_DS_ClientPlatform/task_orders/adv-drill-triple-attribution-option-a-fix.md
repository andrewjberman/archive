<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-adv-drill-triple-attribution-option-a</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status><!-- GO sent 2026-04-14T23:10Z — Andrew lifted pre-presentation hold. DS flips to pending on receipt. -->
    <project_code>ad-hoc</project_code>
    <priority>post-presentation — Andrew GO required</priority>
  </metadata>

  <references>
    <ref type="analysis">docs/analysis/2026-04-14_travis_penfield_adv_aua_triple_attribution_bug.md</ref>
    <ref type="directive">Andrew 2026-04-14 — Option A approved; stage, do not fire until post-presentation</ref>
  </references>

  <objective>
    Patch `data/black_diamond/scripts/gold/D_00b.portal_timeseries.py:806-822` to reuse
    `rel_architect_lookup` as the drill's filter source (not `cdim.primary_architect`).
    Eliminates the $153.6M L0-vs-L1 mismatch on Segment Analytics Continuous-ADV-AUA drill.

    DS's own analysis identified this fix; she owns the scope.
  </objective>

  <scope>
    <file>data/black_diamond/scripts/gold/D_00b.portal_timeseries.py</file>
    <change>
      Exact change per DS analysis section 5.A:

      BEFORE (line 809):
          arch_perf = perf_cohort[perf_cohort['primary_architect'] == arch].copy()

      AFTER:
          travis_rels = set(rel_arch_lookup.loc[
              rel_arch_lookup['architect'] == arch, 'relationship_id'])
          arch_perf = perf_cohort[perf_cohort['relationship_id'].isin(travis_rels)].copy()

      If `rel_architect_lookup` is not in scope at that function, pass it as an
      argument from the caller already consuming it for `nna_aua_by_advisor`.
    </change>
  </scope>

  <acceptance_criteria>
    1. For every architect X emitted in adv_drill: `abs(sum(adv_drill[X].data[-1]) - adv.data[-1][X]) < $1.0`
    2. Travis Penfield specifically: `adv_drill['Travis Penfield'].data[-1]` sums to $391.66M ± $1 (matching L0)
    3. Firm-wide disagreement census in session log — run the one-liner from analysis doc section 6 against current snapshot; report per-architect rel count where rel_architect_lookup disagrees with cdim.primary_architect
    4. Zero change to any other consumer of `perf_cohort['primary_architect']` — geo drill, cla_adv_drill at :844 both untouched. Only the adv_drill block (806-822) is modified
    5. MCP COMPLETE to COO with commit + firm-wide census snippet + Travis spot-check
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io D_00b.portal_timeseries.py` — enumerate all readers/writers; `comp-pipescript consumers cumulative_chart.json` to confirm adv_drill scope.
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
