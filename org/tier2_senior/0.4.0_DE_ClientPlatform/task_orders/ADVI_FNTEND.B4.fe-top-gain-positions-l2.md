<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-14-advi-fntend-b4-fe</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_FNTEND</project_code>
    <wave>C</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 4)</ref>
  </references>

  <objective>
    Stop passing `[]` at `AdvisorBookView.tsx:282` — wire advisor-summary top_gain_positions.
  </objective>

  <acceptance_criteria>
    1. Top Gain Positions renders on advisor L2 with real data (not [])
    2. **Added 2026-04-14 per RD audit:** Top Gain Positions also renders on client L3 drill after AE D_04 PROD re-run (ADVI_PROFAU.006 dependency)
    3. Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`) closed-loop pass on both L2 + L3
    4. MCP COMPLETE to COO
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-transform schema-check AdvisorBookView` + `comp-transform fields AdvisorBookView` (verify top_gain_positions prop actually rendered, not just typed — added 2026-04-14 per CTO audit).
    Phase 3: Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`) on AdvisorBookView.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_FNTEND.B4 DS" status="staged"/>
  </dependencies>

  <cross_domain_coordination>AdvisorBookView.tsx shared with B1/B5 — sequence commits.</cross_domain_coordination>

  <frontend_dev_note>
    If no constitution exists at `portal/.frontend-dev/testing/` for the target component + scenario, author one first per the schema in that directory's README.md. Do not hand-roll Playwright scripts in repo root — the smoke-test.py/.mjs pattern is deprecated.
  </frontend_dev_note>
</task_order>
