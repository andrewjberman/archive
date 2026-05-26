<task_order>
<metadata>
  <to_id>YALP_CORREL.001</to_id>
  <project>YALP_CORREL</project>
  <title>Correlation endpoint + field mapping (Level 1; 1 component; pairwise universe)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~C</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending — GO dispatch this cycle</status>
  <priority>HIGH (Andrew sovereign direct 2026-05-26 ~16:15Z YALP per-page mandate; ~17:00Z countermand; AS-SPAWNED tilde-lanes proceed)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_CORREL.md v0.1 canonical (1.0.0_SA_CTO).</ref>
    <ref type="methodology_template">YALP_MKTOVR.001 (COMPLETE 2026-05-26 cc4a3d575).</ref>
    <ref type="countermand">Andrew sovereign 2026-05-26T~17:00Z: "no dont kill let it go, doesn tmatter its fine".</ref>
  </references>
  <dependencies>
    <dependency>None — AC9-INDEPENDENT.</dependency>
  </dependencies>
</metadata>

<scope>
Per PRD §1 + YALP_MKTOVR methodology: enumerate ticker universe + correlation-pair set + Yang window methodology rendered by Correlation component; trace endpoint → S3 key → producer → upstream → YCharts equivalent. Populate Level-1 table inline in `docs/briefs/yalp_correl_correlation_field_comparison_<T*>.md`.

**1 component in scope:**
1. **Correlation** (`useCorrelationData`) — pairwise rolling correlations on per-asset return series; `correlation_data.json` (`yang-generate-correlation` Lambda; rubric `dc_index` from `data.pkl`).

**Correlation is a derived metric.** YCharts side requires (a) per-ticker price/return series + (b) downstream computation matching Yang's window methodology. Per-ticker series is what TO-002 pulls; pairwise correlation is computed downstream on TO-004 Level-2 side.

**This is mapping work, NOT cutover.** Compute-heavier than other YALP per-page probes (TO-004 ~4-6h vs ~3-5h for others).
</scope>

<acceptance_criteria>
- AC1: Ticker universe enumerated from `correlation_data.json` (full set; per-ticker count noted).
- AC2: Correlation-pair set enumerated (N-choose-2 from universe OR explicit pair list per Yang output).
- AC3: Yang window methodology documented (rolling-window-size + frequency + price-vs-return basis); explicit citation from `yang-generate-correlation` Lambda source.
- AC4: YCharts per-ticker return series endpoint mapped per ticker (or `n/a — <reason>`); leverage YALP_MKTOVR TO-002 corpus for shared tickers.
- AC5: Brief Level-2 table is empty placeholder (TO-004 scope: compute YCharts-side pairwise correlations + cross-reference with Yang values).
</acceptance_criteria>

<compiler_tools_mandate>
**Phase 1:**
- `comp-platinum page Correlation` — S3 key surface.
- `comp-routes trace /api/general/correlations/...`.
- `comp-platinum reverse json/correlations/correlation_data.json`.
- `comp-blast yang-generate-correlation` — Lambda producer surface.
- `comp-pipescript io yang-generate-correlation` — column gaps + portal consumers.

**Phase 2:** `comp-transform fields Correlation`.

**Phase 3:** Session log with Compiler Tools section.
</compiler_tools_mandate>

<cross_domain_coordination>
- **YALP_MDSRC predecessor:** D2 baseline (71 per-ticker surfaces). Re-use heavily.
- **DRIFT-routing rule:** material DRIFT findings → close-MCP to CTO + COO + Andrew.
- **Lane: 0.2.0_DS_PortfolioAnalytics consult on TO-003** (shared-date + window methodology check ~30min).
- **YALP_MKTOVR TO-002 corpus reuse:** shared tickers leverage existing pulls; minimize cookie-session-eviction load.
</cross_domain_coordination>

<expected_evidence>
- Commit hash for the brief doc creation
- Brief doc path: `docs/briefs/yalp_correl_correlation_field_comparison_<T*>.md`
- Ticker universe + pair-set enumerated
- Yang window methodology documented
- Compiler-tools section in session log
</expected_evidence>

<notes>
TO dispatched per Andrew countermand ~17:00Z reversing 16:45Z lane-correction. AS-SPAWNED DS 0.1.0~C canonical; do NOT route to DS 0.2.0~B.

**TO sequence per PRD §4:** TO-001 (THIS) → TO-002 → TO-003 → TO-004 → TO-005 → TO-VAL.

Sister tilde-lanes (~A/~B/~D/~E) run in parallel; per-page probes are AC9-INDEPENDENT + parallel-compatible.

Fast-lane regime applies; ~50min wall precedent (YALP_MKTOVR).
</notes>
</task_order>
