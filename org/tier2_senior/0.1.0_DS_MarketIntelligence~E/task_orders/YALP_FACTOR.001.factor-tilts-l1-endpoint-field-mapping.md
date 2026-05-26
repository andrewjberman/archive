<task_order>
<metadata>
  <to_id>YALP_FACTOR.001</to_id>
  <project>YALP_FACTOR</project>
  <title>FactorTilts endpoint + field mapping (Level 1; 3-tier; scope-pivot: 6 factor SPREADS not 7 MSCI factors)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~E</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete</status>
  <completion>
    <commit>115ad2d40</commit>
    <date>2026-05-26</date>
    <evidence>
      - Brief: docs/briefs/yalp_factor_factortilts_field_comparison_2026-05-22.md (18-section consolidated single-doc; 655 line ship)
      - Spreadsheet: docs/briefs/yalp_factor_side_by_side_spreadsheet_2026-05-22.md + .csv (43 rows)
      - Session log: org/tier2_senior/0.1.0_DS_MarketIntelligence/logs/2026-05-26/yalp_factor_end_to_end.md
    </evidence>
    <ac_scorecard>
      - AC1: PASS — 6 factor spreads hybrid Level-1 rows populated (brief §2.3 Tier-2 rendered fields + §3 C5 constituent map + §14 per-spread verdicts)
      - AC2: PASS — constituent-index map populated per spread; brief §3 C5-ratified factor pair constituents (10 distinct indices: MSCI ACWI / Bloomberg Aggregate / Russell 1000 Growth + Value / MSCI USA / MSCI ACWI ex US / Russell 1000 + 2000 / Bloomberg HY / Bloomberg 1-3yr Gov/Credit) with BBG + YCharts symbol columns
      - AC3: PASS — per-tier sub-sections in brief §2.2 (Tier 1) + §2.3 (Tier 2) + §2.4 (Tier 3) document every rendered field's methodology evidence
      - AC4: EXCEEDED — Level-2 placeholder replaced with full Level-2 verdicts via D3 §A predecessor-as-Level-2-evidence carry-forward (cascade ship of TO-001+002+004+005+VAL per Andrew direct precedent on YALP_MKTOVR; ws COO ENDORSE 17:08Z fast-lane regime applies)
      - AC5: PASS — regression coefs rows tagged GAP-class with explicit sourcing/methodology per row (brief §14.2 + spreadsheet CSV rows 13-43 explicitly "n/a out-of-cutover-scope")
    </ac_scorecard>
    <cascade_note>This TO-001 + TO-002 + TO-004 + TO-005 + TO-VAL all shipped in single commit 115ad2d40 (~50min wall vs PRD ~10-15h = ~12-18x compression). Methodology: YALP_MKTOVR v0.4 template + YALP_MDSRC.D3 §A WS-2 factor-spread reconcile predecessor-as-Level-2-evidence carry-forward at same T*=2026-05-22. Per-spread verdicts: 4 CONFIRMED-MATCH + 2 CONFIRMED-REPRESENTATIVE + 0 DRIFT + 0 NO-TRUST. Regression layer n/a out-of-cutover-scope. ws CTO PRD v0.2 SHIPPED 3fcb76da1 in parallel-convergence with this brief (5th-fire self-correction-upstream pattern banked).</cascade_note>
    <ravc2>RAVC2-Request to ws COO MCP'd 17:30Z; /verify-channel to ws CVO MCP'd 17:31Z; awaiting RAVC2-ACCEPT + 3-step atomic project-close + CVO LD-0086 4-shape verdict.</ravc2>
  </completion>
  <priority>HIGH (Andrew sovereign direct 2026-05-26 ~16:15Z YALP per-page mandate; ~16:42Z ~E-specific reversal "No you continue, we are reversing that order, you've already started"; ~17:00Z broader countermand AS-SPAWNED-lanes-proceed)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_FACTOR.md v0.1 canonical (1.0.0_SA_CTO); PRD §3 scope-pivot pending v0.2 amendment (factor SPREADS not raw MSCI factors per ~E Phase-1a empirical finding ~16:50Z).</ref>
    <ref type="methodology_template">YALP_MKTOVR.001 (COMPLETE 2026-05-26 cc4a3d575).</ref>
    <ref type="andrew_direct_reversal">Andrew sovereign 2026-05-26T~16:42Z: "No you continue, we are reversing that order, you've already started and it's more important we get the work done." — overrides 16:24Z `02519793e` Pod-2 routing for ~E lane.</ref>
    <ref type="countermand">Andrew sovereign 2026-05-26T~17:00Z broader: "no dont kill let it go, doesn tmatter its fine" — countermands 16:45Z lane-correction across all 5 PRDs.</ref>
  </references>
  <dependencies>
    <dependency>None — AC9-INDEPENDENT. Work in flight since ~16:42Z; this TO file ratifies retroactively.</dependency>
  </dependencies>
</metadata>

<scope>
Per PRD §1 + ~E Phase-1a scope-pivot finding + YALP_MKTOVR methodology: enumerate every field rendered by FactorTilts page (3-tier); trace endpoint → S3 key → producer → upstream → YCharts equivalent. Populate Level-1 hybrid table inline in `docs/briefs/yalp_factor_factortilts_field_comparison_<T*>.md` (T*=2026-05-22 confirmed from empirical S3 fetch).

**3-tier components in scope:**
1. **FactorTilts page-mount snapshot** — current factor-tilt positioning + tier-1 summary cards; `tier1-snapshot.json` (~46KB).
2. **Factor Spreads tab** — per-spread time-series + ranking; `tier2-spreads.json` (~196KB).
3. **Time Series toggle** — full historical factor performance series; `tier3-timeseries.json` (~2.1MB).

**Single producer Lambda** (`yang-generate-factor-tilts`); 3-tier output.

**SCOPE-PIVOT ENDORSED** per ~E Phase-1a finding 16:50Z (self-correction-upstream 5th-fire today candidate; sister to YALP_MACROS PRD v0.2 amendment ~17:05Z):

PRD §3 cites 7 MSCI USA factors (Momentum/Quality/Value/Growth/MinVol/Size/DivYield, D2-CONFIRMED-REPRESENTATIVE NTR-variant). **Empirical: portal renders 6 factor SPREADS** (long-short return spreads, not raw MSCI factor index values):
- Equity vs FI / Growth vs Value / US vs Foreign / Large vs Small / Agg vs Short / HY vs Agg

Plus regression coefficients (Tier 1 + Tier 3 `modelTiltTimeSeries`): per-model × per-window β + R² + α against the 6 spreads. **Regression coefs are GAP-class** (no YCharts equivalent — derived from proprietary Opal model portfolio returns).

**Hybrid Level-1 scope (Andrew-spirit preserving field-level cutover-trust):**

For each of 6 factor spreads, columns: (A) Component / surface (page-mount summary table / radar chart / Bars tab / Factor Spreads tab / Time Series toggle) (B) Yang PKL field (`factor_spread['Equity vs FI']` etc.) (C) S3 key + portal endpoint (3-tier: tier1-snapshot / tier2-spreads / tier3-timeseries) (D) Producer Lambda + L1 atomic-field-grain rubric (FACTOR_SPREADS per L1 §6.7-6.9) (E) **Constituent index map** — long-side index + short-side index that compute each spread; map from yang model PKL preparation source (F) YCharts equivalent — per-constituent index + reconstructed spread method (G) Regression coefs (Tier 1) — marked `n/a — GAP-class; derived from proprietary Opal model portfolio returns; no YCharts equivalent` per YALP_MKTOVR `n/a out-of-cutover-scope` precedent (Daily Cloud + F&G + Trending Topics).

**Level-2 scope (TO-004):** verify 6 spread VALUES on T*=2026-05-22 by reconstructing from constituents via YCharts pulls. Regression coefs out of Level-2 scope.

**PRD §3 amendment ask routes to ws CTO** in parallel (~E MCP'd CTO 16:50Z); this TO ships under PRD v0.1 + ~E's hybrid-scope-finding inline; CTO ratify can amend PRD v0.2 without blocking TO-001 ship.

**This is mapping work, NOT cutover.**
</scope>

<acceptance_criteria>
- AC1: Each of 6 factor spreads has hybrid Level-1 row populated (columns A-G).
- AC2: Constituent-index map populated per spread (long-side index + short-side index from yang model PKL preparation source).
- AC3: Per-component sub-section in the brief documents methodology evidence per field (compiler tool surfaced).
- AC4: Brief Level-2 table is an empty placeholder.
- AC5: Regression coefs rows tagged GAP-class with explicit `sourcing/methodology` documentation per row (consistent with YALP_MKTOVR n/a-precedent).
</acceptance_criteria>

<compiler_tools_mandate>
**Phase 1:**
- `comp-platinum page FactorTilts` — S3 key surface (3-tier outputs).
- `comp-routes trace /api/general/factor-tilts/...`.
- `comp-platinum reverse` each tier S3 key.
- `comp-blast yang-generate-factor-tilts` — producer surface.
- `comp-pipescript io yang-generate-factor-tilts` — column gaps; **also surface model PKL preparation source path** (constituent enumeration upstream).

**Phase 2:** `comp-transform fields FactorTilts`.

**Phase 3:** Session log with Compiler Tools section + [[spawn-with-direction-fast-orient-pattern]] refinement-candidate banking note (verify routing against latest origin commits AFTER reading PRD, BEFORE first MCP).
</compiler_tools_mandate>

<cross_domain_coordination>
- **YALP_MDSRC predecessor:** D2 baseline 7 MSCI factor surfaces (NTR-variant). The hybrid pivot RECONCILES D2 (factors) vs portal-rendered (spreads from constituent factors).
- **DRIFT-routing rule:** material DRIFT findings → close-MCP to CTO + COO + Andrew. **Regression coefs = GAP-class NOT DRIFT.**
- **Lane: 0.2.0_DS_PortfolioAnalytics consult on TO-003** — T*=2026-05-22 already empirically confirmed by ~E from S3 fetch; TO-003 may shorten / no-op.
- **PRD §3 amendment** — ws CTO ratify in parallel (no block on TO-001 ship; brief inline-documents the pivot).
</cross_domain_coordination>

<expected_evidence>
- Commit hash for the brief doc creation
- Brief doc path: `docs/briefs/yalp_factor_factortilts_field_comparison_2026-05-22.md`
- 6-spread × 7-column Level-1 hybrid table populated
- Constituent-index map per spread
- Compiler-tools section in session log
- Banking note for [[spawn-with-direction-fast-orient-pattern]] refinement candidate
</expected_evidence>

<notes>
Work in flight since Andrew direct reversal ~16:42Z. This TO file ratifies retroactively + provides AC discipline; ~E may have already shipped brief Phase 1 by file landing time — that's fine, per `[[standby-prep-compress-to-delivery-when-context-sufficient]]` compression with PRD-method-author advantage (~E inherits YALP_MKTOVR methodology authored same agent-class).

**TO sequence per PRD §4 + ~E hybrid:** TO-001 (THIS) → TO-002 YCharts constituent-pulls → TO-003 may no-op (T* confirmed) → TO-004 Level-2 6-spread VALUE verification + GAP coefs ack → TO-005 spreadsheet → TO-VAL consolidated.

**Pattern banking absorbed (this TO body):** [[spawn-with-direction-fast-orient-pattern]] refinement — verify routing against latest origin commits AFTER PRD read + BEFORE first MCP. Doctrine-worthy; surface in /mstr-review next cycle as v0.2-candidate refinement.

**Andrew direct reversal class:** 5th distinct trigger pattern today (sister to self-correction-upstream + CORROBORATE Path-A-AMEND + ALLOCATION-REVISION-PRE-CONFIRMATION + ALLOCATION-REVISION-VOIDED-BY-ANDREW). Andrew sovereign post-spawn reversal on specific agent-instance lane (16:42Z ~E-specific) preceding broader 17:00Z fabric-wide countermand. Worth /govern surface.

Fast-lane regime applies.
</notes>
</task_order>
