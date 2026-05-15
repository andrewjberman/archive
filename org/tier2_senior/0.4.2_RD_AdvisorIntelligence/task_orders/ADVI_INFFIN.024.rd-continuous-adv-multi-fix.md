<task_order>
  <metadata>
    <id>ADVI_INFFIN.024</id>
    <slug>rd-continuous-adv-multi-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-05-14</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>RD 0.4.2 bench-clear post H3 FE patch close. Wave 1 RD batch.</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — Continuous ADV view 4-fix bundle; Andrew direct walkthrough</priority>
    <sla>~2-3h wall actual per Pod 4 velocity</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFFIN_UX_FIXES_BATCH.md §3.5 (CTO `23fdaac67`)</ref>
    <ref type="andrew_direct">Andrew 2026-05-14 ~23:0XZ image #6: 4-item list (Other label / sidebar metrics / HH IDs / clickthrough)</ref>
    <ref type="surface">Inflection portal → AdvisorIntelligence → Segment Analytics → Distribution → Continuous → ADV cohort</ref>
    <ref type="hh_grain">[[project_inflection_advisor_structure]] HH-grain framework; [[project_inflec_frontend_dev_auth_path]] Option C internal access supports HH-ID-not-pseudonymized scope</ref>
  </references>

  <context>
    Per COO Q2 routing decision: SINGLE multi-fix TO with 4 ACs (not split into 4 sub-TOs). Same surface (Continuous ADV), same lane (RD), same wall (~2-3h). Cohesive scope; 4x RAVC overhead avoided.

    4 sub-fixes:
    - §3.5a: gray bar entries labeled "Other" (not "Client")
    - §3.5b: sidebar metrics calc fix (Since May 2025 / Growth Rate / New Clients — all currently $0/0%/0)
    - §3.5c: HH IDs replace "Client 5/6/7..." pseudonyms
    - §3.5d: HH ID clickthrough → advisor book page for that HH
  </context>

  <objective>
    Single multi-fix TO addressing 4 Continuous ADV view issues. AC1-AC4 = empirical verification per sub-fix.
  </objective>

  <scope>
    <files>
      <file action="modify">portal FE — Continuous view stacked bar chart component (legend + tooltip + sidebar listing)</file>
      <file action="modify">portal FE — Continuous view sidebar metrics calculations (Since May 2025 / Growth Rate / New Clients)</file>
      <file action="modify">portal FE — Continuous view HH ID rendering + routing</file>
      <file action="readonly_reference">existing advisor book page route + book.json data path</file>
    </files>
  </scope>

  <phase id="1" when="§3.5a Other label">
    <step>
      <run>grep FE for Client legend label + tooltip + sidebar listing; identify gray bar segment data source (aggregated remainder of clients beyond top-N)</run>
      <expect>Sources surfaced.</expect>
    </step>
    <step>
      <run>Relabel gray entries from "Client" to "Other" in legend + tooltip + sidebar</run>
      <expect>All 3 surfaces show "Other" for gray segment.</expect>
    </step>
  </phase>

  <phase id="2" when="§3.5b Sidebar metrics">
    <step>
      <run>Inspect sidebar metric calculations: Since May 2025 cumulative NNA / Growth Rate CAGR / New Clients count; identify why currently $0/0%/0</run>
      <expect>Calculation pipeline issue surfaced (FE memo bug OR backend emit gap).</expect>
    </step>
    <step>
      <run>Fix calculations OR cascade to DS if emit gap confirmed (cascade TO INFFIN.024b for DS lane)</run>
      <expect>Metrics correctly calculated OR cascade routed.</expect>
    </step>
  </phase>

  <phase id="3" when="§3.5c HH IDs">
    <step>
      <run>Replace "Client 5/6/7..." pseudonyms with HH IDs throughout continuous ADV view (legend + tooltip + sidebar). Per [[project_inflection_advisor_structure]] HH-grain framework + Option C internal access</run>
      <expect>HH IDs rendered; no pseudonymization for Inflection.</expect>
    </step>
    <step>
      <run>49F regression: 49F continuous ADV view should NOT show HH IDs (49F retains pseudonymization OR uses different grain); verify per-partner conditional rendering</run>
      <expect>49F regression PASS.</expect>
    </step>
  </phase>

  <phase id="4" when="§3.5d Clickthrough">
    <step>
      <run>Wire HH ID click handler to navigate to advisor book page for that HH; URL pattern per existing routing convention (likely /advisor-intelligence/inflection/advisors/{advisor_key}/books/{hh_id})</run>
      <expect>Click navigation works; book page renders for clicked HH.</expect>
    </step>
    <step>
      <run>GEO cohort regression: verify continuous GEO view (state/city labels) unchanged; no regression on non-ADV cohorts</run>
      <expect>GEO regression PASS.</expect>
    </step>
  </phase>

  <phase id="5" when="commit + RAVC">
    <step>
      <run>Visual smoke: full continuous ADV view 4-fix verification; sidebar metrics non-zero; HH IDs render; click navigates</run>
      <expect>All 4 sub-fixes visually verified.</expect>
    </step>
    <step>
      <run>safe-commit.sh per Rule 14a + Author identity RD 0.4.2</run>
      <expect>Commit clean.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + DT 0.4 (PROD promote candidate)</run>
      <expect>Evidence-bearing close + 4 sub-fix attestation.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1 (§3.5a): Gray bar entries labeled "Other" in legend + tooltip + sidebar
    AC2 (§3.5b): Sidebar metrics calculate correctly (Since May 2025 / Growth Rate / New Clients) OR cascade TO INFFIN.024b authored for DS
    AC3 (§3.5c): Client pseudonyms replaced with HH IDs throughout continuous ADV view
    AC4 (§3.5d): HH ID click navigates to advisor's book page for that HH
    AC5: GEO cohort regression PASS (state/city labels unchanged)
    AC6: 49F regression PASS (no Inflection-only behavior leaked to 49F)
    AC7: Visual smoke evidence for all 4 sub-fixes
    AC8: No emoji per CLAUDE.md
    AC9: RAVC2 to COO + CC CTO + DT 0.4
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1-4 comp-transform schema-check + grep + edit; Phase 5 safe-commit.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: RD H3 FE patch close.
    PARALLEL-OK: All other INFFIN.019-028 sibs.
    POTENTIAL CASCADE: §3.5b emit gap spawns INFFIN.024b for DS lane.
    NO 49F REGRESSION.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>FE-only; cascade DS path if needed.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. §3.5a Other label
    2. §3.5b sidebar metrics fix OR cascade
    3. §3.5c HH IDs
    4. §3.5d clickthrough wired
    5. GEO + 49F regression evidence
    6. RAVC2 with 4 sub-fix attestation
  </deliverables>

  <ravc>RD 0.4.2 RAVC2 to COO + CC CTO + DT 0.4 on AC1-9 PASS.</ravc>

  <notes>
    **Author identity:** `--author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>"`.

    **Why single TO not 4:** cohesive surface scope + same agent + same wall = 4x RAVC overhead avoidance per COO Q2 routing decision.

    **HH ID exposure scope:** Inflection internal access (Option C) supports HH-grain visibility. 49F retains pseudonymization OR different grain per [[project_inflection_advisor_structure]] vs 49F-150-advisor structure.

    **No emoji per CLAUDE.md.**
  </notes>
</task_order>
