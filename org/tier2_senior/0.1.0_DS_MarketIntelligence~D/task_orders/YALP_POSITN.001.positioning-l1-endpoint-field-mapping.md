<task_order>
<metadata>
  <to_id>YALP_POSITN.001</to_id>
  <project>YALP_POSITN</project>
  <title>Positioning endpoint + field mapping (Level 1; 2 components; GAP-heavy)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~D</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete</status>
  <priority>HIGH (Andrew sovereign direct 2026-05-26 ~16:15Z YALP per-page mandate; ~17:00Z countermand; AS-SPAWNED tilde-lanes proceed)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_POSITN.md v0.1 canonical (1.0.0_SA_CTO).</ref>
    <ref type="methodology_template">YALP_MKTOVR.001 (COMPLETE 2026-05-26 cc4a3d575).</ref>
    <ref type="countermand">Andrew sovereign 2026-05-26T~17:00Z: "no dont kill let it go, doesn tmatter its fine".</ref>
  </references>
  <dependencies>
    <dependency>None — AC9-INDEPENDENT.</dependency>
  </dependencies>
</metadata>

<scope>
Per PRD §1 + YALP_MKTOVR methodology: enumerate every field rendered by each of the 2 Positioning page components; classify each as YCharts-comparable vs GAP-class upfront. Populate Level-1 table inline in `docs/briefs/yalp_positn_positioning_field_comparison_<T*>.md`.

**2 components in scope:**
1. **Positioning main + PositioningSummary panel** — asset-class allocation + sub-component breakdown; `positioning_data.json` (`yang-generate-positioning` Lambda; `data.pkl` + `model.pkl` + cross-pipeline `aum-metrics.json`).
2. **HoldingsTab** — per-holding allocation + classification; `holdings_attribution_data.json` (`yang-generate-holdings-attribution` Lambda; `attribution_excel` + ETF DynamoDB classifications).

**GAP-heavy probe (PRD §3):** per-row verdict mix ~30-50% MATCH-class (index returns) + ~50-70% GAP-class (Yang/BD-internal allocation metadata). `holdings_attribution_data.json` upstream is internal-only (attribution_excel manual workbook + ETF classifications DynamoDB; NOT Bloomberg-pulled).

**This is mapping work, NOT cutover.**
</scope>

<acceptance_criteria>
- AC1: Every rendered field on both 2 components has a Level-1 row populated in the brief doc.
- AC2: YCharts-equivalent column is either a real endpoint+field OR an explicit `n/a — <reason>` (no blanks). GAP-class rows tagged explicitly.
- AC3: Per-component sub-section in the brief documents the methodology evidence per field.
- AC4: Brief doc Level-2 table is an empty placeholder.
- AC5: GAP-class classification surface area documented per-row: index-return rows → MATCH/REPRESENTATIVE; allocation/classification metadata rows → GAP with `sourcing/methodology` documentation.
</acceptance_criteria>

<compiler_tools_mandate>
**Phase 1:**
- `comp-platinum page Positioning` — S3 key surface.
- `comp-routes trace /api/general/positioning/...`.
- `comp-platinum reverse json/positioning/positioning_data.json` + `json/positioning/holdings_attribution_data.json`.
- `comp-blast yang-generate-positioning` + `yang-generate-holdings-attribution` — Lambda producer surface.
- `comp-pipescript io` each producer.

**Phase 2:** `comp-transform fields Positioning` (+ HoldingsTab).

**Phase 3:** Session log with Compiler Tools section.
</compiler_tools_mandate>

<cross_domain_coordination>
- **YALP_MDSRC predecessor:** D2 baseline for index-return surfaces.
- **DRIFT-routing rule:** material DRIFT findings → close-MCP to CTO + COO + Andrew. **For GAP-class rows, route is different:** GAP is NOT DRIFT (no YCharts equivalent exists by design); document via `sourcing/methodology` not via DRIFT-routing.
- **Lane: 0.2.0_DS_PortfolioAnalytics consult on TO-003** (shared-date `T*` determination + cross-pipeline `aum-metrics.json` BD-side timing ~30min).
- **AE 0.7.0 on-call** — likely zero touch.
</cross_domain_coordination>

<expected_evidence>
- Commit hash for the brief doc creation
- Brief doc path: `docs/briefs/yalp_positn_positioning_field_comparison_<T*>.md`
- Level-1 table populated for 2 components
- GAP-class row inventory documented
- Compiler-tools section in session log
</expected_evidence>

<notes>
TO dispatched per Andrew countermand ~17:00Z reversing 16:45Z lane-correction. AS-SPAWNED DS 0.1.0~D canonical; do NOT route to DS 0.2.0~C.

Your prior stand-down session log (org/tier2_senior/0.1.0_DS_MarketIntelligence/logs/2026-05-26/yalp_positn_stand_down_received.md) blocked by owned-paths hook — keep as working-tree-only OR fold the [[spawn-with-direction-fast-orient-pattern]] refinement candidate into THIS TO's session log per Compiler-tools Phase 3 (the "verify routing against latest origin commits AFTER reading PRD, BEFORE first MCP" refinement is doctrine-worthy banking).

**TO sequence per PRD §4:** TO-001 (THIS) → TO-002 → TO-003 → TO-004 (GAP-heavy ~3-5h) → TO-005 → TO-VAL.

Smaller pull surface than MKTOVR per PRD §4 (TO-002 ~1h vs ~2-3h elsewhere); GAP-class concentration shrinks YCharts test-pull set.

Fast-lane regime applies.
</notes>
</task_order>
