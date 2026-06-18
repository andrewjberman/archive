# TO DECK_CLAUDE.CHARTS-B — Scatter / risk-return charts (incl. Peers, Yang request)

<issued_to>0.4.2_RD_AdvisorIntelligence~B</issued_to>
<issued_by>0.4.2_RD_AdvisorIntelligence (base, deck-system owner) — Andrew-direct chart fan-out</issued_by>
<project>DECK_CLAUDE</project>
<status>staged</status>

## Objective
Port the portal's **scatter / risk-return** charts into the Charts family. You own
`deck_generation/engine/archetypes/charts/scatter.py` exclusively (stubbed + wired). Targets + data
shapes in `deck_generation/dev/docs/portal-chart-port-map.md`. Includes **two named priorities**:
the return-vs-volatility scatter and **the Peers chart (a direct request from Yang)**.

## Build these
- **chart-scatter-riskreturn** (PRIORITY) — native XY scatter, x=volatility, y=return; **circle=model,
  diamond=benchmark** (two series, distinct marker styles), per-point Opal colors. Source:
  `portal/src/components/ReturnVolatilityScatter.tsx`. Use `_native.opal_scatter`; set the benchmark series
  marker to diamond.
- **chart-line-rolling** (PRIORITY, the variants) — native line over time; parameterize so ONE archetype
  covers Rolling Sharpe / Capture / Drawdown (+ optional 100% reference line). Source:
  `portal/src/components/RollingSharpeChart.tsx` (+ RollingCaptureChart / MaxDrawdownChart). `opal_chart(s,"line",...)`.
- **chart-quartile-peers** (PRIORITY, **Yang's request**) — SHAPE-BUILT: a p25-p75 box + median line +
  min/max whiskers + the model's marker, per period. Source: `portal/src/pages/ModelPortfolios/tabs/PeersTab.tsx`
  (the `QuartileChart`). Build from C primitives (the stat-stacked pattern), A1 palette.
- **chart-bubble** (optional) — native BUBBLE (x/y/size) if time allows.

## Build protocol
1. **Read first:** `dev/docs/portal-chart-port-map.md`, `DESIGN_BIBLE.md`, `engine/archetypes/charts/_native.py`
   (`opal_scatter`/`opal_chart`), the existing **stat-stacked** archetype (`engine/archetypes/stat/__init__.py`)
   as the shape-built pattern for the Peers quartile, and the portal source files above (extract real data shapes
   + marker conventions). cwd = `deck_generation`.
2. **Edit ONLY** `engine/archetypes/charts/scatter.py` (+ showcase + log). Do NOT edit `_native.py`/`compose.py`/
   `registry.py`/another agent's chart submodule.
3. **Native** via `opal_scatter`/`opal_chart`; **shape-built** (the Peers quartile) via C primitives, A1 palette
   only, true circles via `C.circle`, no white-on-white (B3). **F2: plot ONLY supplied data.** The scatter's two
   marker shapes (circle=model, diamond=benchmark) — set per-series marker style on the chart object.
4. **register()** each (`method="archetypes.charts.<func>"`, `family="Charts"`).
5. **Showcase** `dev/scripts/showcase_charts_scatter.py` — one slide per chart, REAL Opal data (the actual
   model return/vol numbers, real peer quartiles) -> **GATE PASS 0 lint + full coverage**; no consecutive-repeat.
6. **/seams completion gate (REQUIRED — Andrew-direct):** `/seams` each chart archetype on all 3 axes —
   MECHANICAL (generates + renders), DECLARATIVE (registered + claim true + chart TYPE matches), **SEMANTIC**
   (render-grounded: scatter points at the right (vol,return); circle vs diamond correct; the quartile box
   spans p25-p75 with the median + whiskers in the right places; Opal palette). Each must PASS all 3.
7. **Visual-QA** via COM + READ every slide (the scatter marker shapes + the quartile box are the highest-risk).
   Native charts editable (double-click -> data grid).
8. **Self-commit (DECK lane):** pull, `.tools/safe-commit.sh --author "0.4.2_RD_AdvisorIntelligence~B <...~B@opal.agent>"
   -m "...~B: DECK_CLAUDE -- scatter/risk-return chart archetypes + /seams PASS ..." --
   deck_generation/engine/archetypes/charts/scatter.py deck_generation/dev/scripts/showcase_charts_scatter.py`.
   Session log; RAVC2 to base RD CC `2.0.0_SA_COO` with /seams verdicts. (Yang requested the Peers chart — call out
   its /seams SEMANTIC verdict explicitly.)

<acceptance_criteria>
- catalog shows your scatter/risk-return chart archetypes under `Charts`.
- showcase_charts_scatter.py prints GATE PASS, 0 lint, full coverage.
- **/seams PASS on all 3 axes per chart** (Peers SEMANTIC called out) — verdicts in your RAVC2.
- Native charts editable; the Peers quartile reads correctly against real peer data.
- Committed under your ~B author line on the DECK lane.
</acceptance_criteria>

<compiler_tools_mandate>N/A comp-* (deck tooling). Mandated validation = the **/seams** 3-axis pass per chart + design_lint [AUTO] (incl. chart-series A1) + COM visual-QA.</compiler_tools_mandate>
<cross_domain_coordination>`_native.py` shared (base-owned) — call, don't edit. You own `scatter.py`. Pull before commit. Base RD integrates.</cross_domain_coordination>
