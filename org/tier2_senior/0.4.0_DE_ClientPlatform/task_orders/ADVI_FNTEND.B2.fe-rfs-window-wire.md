<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-14-advi-fntend-b2-fe</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_FNTEND</project_code>
    <wave>C</wave>
    <priority>keystone — must land before B3/B4/B5 FE</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 2)</ref>
  </references>

  <objective>
    Rename `AuaDecompositionPanel` → `RelationshipFlowsSummary` with QTD/YTD/Max toggle (default QTD).
    Lift window into shared state. Rebind Accounts table columns to RFS window.
    Add NNA column + window toggle to Clients table.
  </objective>

  <acceptance_criteria>
    1. QTD/YTD/Max toggle visible on Relationship Flows Summary; default QTD
    2. All three panels (RFS, Accounts, Clients) share one window state
    3. NNA column present on Clients table, obeys window toggle
    4. Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`) closed-loop pass
    5. MCP COMPLETE to COO
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-transform schema-check --feature rfsWindow` on RelationshipFlowsSummary + AccountsTable + ClientsTable; `comp-cache collisions` (new window state may introduce new React Query keys — must not collide with existing client/account keys).
    Phase 2: `comp-transform ternary-audit` on all three (window routing).
    Phase 3: Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`).
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_FNTEND.B2 DS" status="staged"/>
  </dependencies>

  <cross_domain_coordination>
    types.ts touched by B1/B2/B3/B4/B5. Sequential FE commits on types.ts.
    AdvisorBookView.tsx shared with B1/B4/B5 — sequence commits.
  </cross_domain_coordination>

  <frontend_dev_note>
    If no constitution exists at `portal/.frontend-dev/testing/` for the target component + scenario, author one first per the schema in that directory's README.md. Do not hand-roll Playwright scripts in repo root — the smoke-test.py/.mjs pattern is deprecated.
  </frontend_dev_note>
</task_order>
