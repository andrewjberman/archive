<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-14-advi-fntend-b8-fe</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_FNTEND</project_code>
    <wave>C</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 8)</ref>
  </references>

  <objective>
    FeeEfficiencyPanel role-filter with client-side RERANK (not filter-hide):

    1. Add role-checkbox ToggleGroup to PanelHeader actions (multi-select; persist across Window toggle changes).
    2. Selector state: `Set<RoleKey>`, initial = all 5 checked.
    3. Derived chartData/sortableData: per advisor, sum `role_breakdown[r].{aua, nna, commission}` over selected roles. `fee_bps` = commission/AUA-weighted average of selected roles. Drop advisors with zero activity across selected roles.
    4. **Recompute `efficiency_pctile` client-side on the filtered population** — rank by `commission/NNA` ratio, negative-NNA bucket at bottom (matches current tooltip helper text). 1-100 scale, stable tie-break.
    5. Log-log regression already recomputes on chartData — automatic.
    6. Tooltip + table reflect recomputed values; add "ranked within selected roles" to helptext.
  </objective>

  <acceptance_criteria>
    1. Five role checkboxes visible in PanelHeader actions, all checked by default
    2. Unchecking reduces dataset AND updates percentile ranks (visible advisor movement, not row-hide)
    3. Empty selection → empty-state message "Select at least one role"
    4. Role filter persists across Window/Period toggle changes
    5. Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`) closed-loop pass
    6. Sum-reconciliation: with all 5 selected, metrics match production within $0.01
    7. MCP COMPLETE to COO
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-transform schema-check FeeEfficiencyPanel --feature roleFilter`; `comp-transform ternary-audit FeeEfficiencyPanel` (role routing chains); `comp-cache collisions` (auto-rule: new FE state driving React Query — role selection may introduce query-key hash).
    Phase 2: `comp-transform ternary-audit` final pass.
    Phase 3: Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`).
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_FNTEND.B8 DS" status="staged"/>
  </dependencies>

  <cross_domain_coordination>
    FeeEfficiencyPanel is N1 panel, DE-scope (not RD). types.ts shared with B1/B2/B3/B4/B5 — sequence commits.
  </cross_domain_coordination>

  <frontend_dev_note>
    If no constitution exists at `portal/.frontend-dev/testing/` for the target component + scenario, author one first per the schema in that directory's README.md. Do not hand-roll Playwright scripts in repo root — the smoke-test.py/.mjs pattern is deprecated.
  </frontend_dev_note>
</task_order>
