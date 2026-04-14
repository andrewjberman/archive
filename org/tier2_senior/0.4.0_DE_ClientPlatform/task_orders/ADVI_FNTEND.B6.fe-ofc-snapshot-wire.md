<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-14-advi-fntend-b6-fe</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_FNTEND</project_code>
    <wave>C</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 6)</ref>
  </references>

  <objective>
    Wire time-machine strip on OfcAdvisorListPanel (mirror L0).
    Render NNA bell curve in the right partition for OFC at L0 + L1.
  </objective>

  <acceptance_criteria>
    1. Austin OFC donut segment shows advisor list on L1
    2. NNA bell curve renders on L0 OFC partition
    3. NNA bell curve renders per-office on L1
    4. time-machine strip works on L1 OfcAdvisorListPanel
    5. Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`) closed-loop pass
    6. MCP COMPLETE to COO
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-transform schema-check DistributionTab --feature ofcSnapshot` + `comp-transform ternary-audit DistributionTab`.
    Phase 3: Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`) on DistributionTab OFC mode.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_FNTEND.B6 DS" status="staged"/>
  </dependencies>

  <cross_domain_coordination>DistributionTab.tsx touched only by B6 — no coordination needed.</cross_domain_coordination>

  <frontend_dev_note>
    If no constitution exists at `portal/.frontend-dev/testing/` for the target component + scenario, author one first per the schema in that directory's README.md. Do not hand-roll Playwright scripts in repo root — the smoke-test.py/.mjs pattern is deprecated.
  </frontend_dev_note>
</task_order>
