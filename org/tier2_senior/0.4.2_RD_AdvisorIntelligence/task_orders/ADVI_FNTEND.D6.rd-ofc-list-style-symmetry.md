<task_order>
  <metadata>
    <id>0.4.2_RD_AdvisorIntelligence-2026-04-14-advi-fntend-d6</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-14</date>
    <status>pending</status><!-- CONDITIONALLY COMPLETE — fix applied (fallback-branch div → GEO/ADV container metrics); awaiting /frontend-dev closed-loop pass per RAVC (RD-triggered run requested 2026-04-14T21:31Z). Flip to complete when RD confirms clean run. -->
    <project_code>ADVI_FNTEND</project_code>
    <wave>A</wave>
    <type>FE-trivial follow-on</type>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 0 follow-on)</ref>
    <ref type="b0_predecessor">ADVI_FNTEND.B0 (portal DEV 5ea017c) — this TO landed before D6 was flagged</ref>
  </references>

  <objective>
    Style symmetry fix (added 2026-04-14 per Andrew post-B0 ship). The office-list text
    in Continuous-OFC-AUA does NOT match the text size/styling of Continuous-GEO-AUA
    and Continuous-ADV-AUA. Fix for visual parity across all three cohorts.

    Location: `DistributionTab.tsx` `ContinuousChartView` — the cohort-ternary branch
    rendering the OFC list. Find the GEO/ADV list `className` set; apply the same
    set to the OFC branch.
  </objective>

  <acceptance_criteria>
    1. OFC office-list font-size matches GEO/ADV exactly (at L0 and drilled views)
    2. OFC office-list font-weight matches
    3. OFC office-list color matches
    4. OFC office-list spacing (padding/margin) matches
    5. Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`) pass on DistributionTab OFC + GEO + ADV Continuous views — visual symmetry confirmed
    6. MCP COMPLETE to COO with commit hash
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-transform schema-check DistributionTab` (confirm no className/prop drift on the OFC branch).
    Phase 2: Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`).
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>
</task_order>
