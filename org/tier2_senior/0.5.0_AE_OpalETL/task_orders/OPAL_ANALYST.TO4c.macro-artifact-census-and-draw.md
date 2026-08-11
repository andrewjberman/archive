# OPAL_ANALYST.TO4c — Macro artifact census + /draw (vertical 3)

<task_order>
<id>OPAL_ANALYST.TO4c</id>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued_to>0.5.0_AE_OpalETL~Z</issued_to>
<date>2026-08-10</date>
<status>complete</status>
<!-- ACCEPTED 2026-08-10 1925Z, 2.0.0_SA_COO~Z. Census @5efce36b7 (parse clean; 84-key
     denominator itemized incl. the 79-slug timeseries family, unrendered + frozen rows
     explicit); /draw @9e89e119c delivered. Discipline flag HONORED: all evidence first-hand,
     in-flight Explore output discarded, note in census header. COO spot-check at portal
     source: MacroHeatmap.tsx:136-143 + YieldCurveTab.tsx:289-290 both exact. Residuals
     routed: third vintage variant (as_of, timeseries family) -> CTO~Z census_ref design;
     vix_data.json superseded-but-published-daily (zero callers) -> MSTR~Z surprise channel
     as decommission candidate, no action taken (exclusivity). -->

<priority>P1</priority>

<references>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md §8.1 grammar @7753e1caf</ref>
  <ref type="pilot">ARTIFACT_CENSUS_MP.yaml @0c1dae3da (ratified template) + TO-4b's POD2 census</ref>
  <ref type="ruling">Andrew verticals-2-4 GO @95b3e2852; plan @6c1161075</ref>
</references>

<dependencies>
  <dependency agent="0.5.0_AE_OpalETL~Z" task="OPAL_ANALYST.TO4b" status="complete"/>
  <!-- Sequential per Andrew's ruled order. Batch GO covers it: on TO-4b report, flip this
       to pending and begin WITHOUT a new GO. -->
</dependencies>

<scope>
Vertical 3, identical shape to TO-4b with target = every portal-served MACRO artifact:
(1) `refs/census/ARTIFACT_CENSUS_MACRO.yaml` — same grammar, five rules, ratified pilot
choices; (2) /draw of complete findings to MSTR~Z (for Andrew) cc COO~Z.
</scope>

<compiler_tools_mandate>
Same three-phase triad as TO-4b, target macro: Phase 1 comp-estate macro thread(s) +
PORTAL_RETRIEVAL frame (denominator before rows); Phase 2 parse + five-rule self-score;
Phase 3 complete /draw + report (commit + denominator + delivery pointer).
</compiler_tools_mandate>

<cross_domain_coordination>
Same as TO-4b: new refs/census/ file, audited lane-override, read-only estate access.
</cross_domain_coordination>

<acceptance_criteria>
Same five as TO-4b, target ARTIFACT_CENSUS_MACRO.yaml.
</acceptance_criteria>

<notes>
Sequential batch member: begins on TO-4b completion, no new GO. Then proceed to TO-4d.
</notes>
</task_order>
