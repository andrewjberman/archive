# TO DECK_CLAUDE.CHARTS-D — Line / area + matrix charts (heatmap / treemap)

<issued_to>0.4.2_RD_AdvisorIntelligence~D</issued_to>
<issued_by>0.4.2_RD_AdvisorIntelligence (base, deck-system owner) — Andrew-direct chart fan-out</issued_by>
<project>DECK_CLAUDE</project>
<status>complete</status>

## Objective
Port the portal's **line / area + matrix** charts into the Charts family. You own
`deck_generation/engine/archetypes/charts/series.py` exclusively (stubbed + wired). Targets + data
shapes in `deck_generation/dev/docs/portal-chart-port-map.md`. Includes a named priority: the Model
Portfolios **surface** (stacked-area allocation trend).

## Build these
- **chart-line-timeseries** — Macroeconomics indicators over time (multi-series line). Source:
  `portal/src/pages/Macroeconomics/`. Native `opal_chart(s,"line",dates,[(name,vals),...])`, multi-series A1.
- **chart-area-stacked** (PRIORITY, MP "surface") — stacked-area allocation/cumulative trend. Source:
  `portal/src/pages/ModelPortfolios.tsx`. Native `opal_chart(s,"area_stacked",...)`, ramp dark->light.
- **chart-heatmap** — Correlation matrix (-1..1). Source: `portal/src/pages/Correlation/`. **SHAPE-BUILT**
  (python-pptx has no heatmap): a colored cell grid via C primitives, **navy<->cool-grey<->purple diverging**
  (A1 only — no red/green), value labels, axis labels.
- **chart-treemap** — Attribution / Positioning weights. Source: `portal/src/pages/Attribution/` or
  `Positioning/`. **SHAPE-BUILT**: nested rectangles sized by weight, ramp dark->light, labels.

## Build protocol
1. **Read first:** `dev/docs/portal-chart-port-map.md`, `DESIGN_BIBLE.md`, `engine/archetypes/charts/_native.py`
   (`opal_chart`), the existing **grid-matrix** + **table** archetypes (`engine/archetypes/grid/__init__.py`,
   `C.table` in `engine/compose.py`) as the shape-built patterns for the heatmap/treemap, and the portal source
   files above (real data shapes). cwd = `deck_generation`.
2. **Edit ONLY** `engine/archetypes/charts/series.py` (+ showcase + log). Do NOT edit `_native.py`/`compose.py`/
   `registry.py`/another agent's submodule.
3. **Native** via `opal_chart` (line / area_stacked); **shape-built** (heatmap/treemap) via C primitives.
   **A1 palette ONLY** — the heatmap diverging scale is navy (high +) <-> cool-grey (0) <-> purple (low -)
   since there is no red/green in the bible. **F2: plot ONLY supplied data.** No white-on-white (B3).
4. **register()** each (`method="archetypes.charts.<func>"`, `family="Charts"`).
5. **Showcase** `dev/scripts/showcase_charts_series.py` — one slide per chart, REAL Opal data (real macro
   series, real allocation trend, a real correlation matrix, real attribution weights) -> **GATE PASS 0 lint
   + full coverage**.
6. **/seams completion gate (REQUIRED — Andrew-direct):** `/seams` each chart on all 3 axes — MECHANICAL
   (generates + renders), DECLARATIVE (registered + claim true + chart TYPE matches), **SEMANTIC** (render-grounded:
   line series track the real values; the stacked area sums correctly; the heatmap cell colors map monotonically
   to the correlation values; treemap rect AREAS are proportional to the weights; Opal diverging palette). Each PASS all 3.
7. **Visual-QA** via COM + READ every slide (the heatmap diverging mapping + the treemap proportionality are highest-risk).
   Native charts editable (double-click -> data grid).
8. **Self-commit (DECK lane):** pull, `.tools/safe-commit.sh --author "0.4.2_RD_AdvisorIntelligence~D <...~D@opal.agent>"
   -m "...~D: DECK_CLAUDE -- line/area+matrix chart archetypes + /seams PASS ..." --
   deck_generation/engine/archetypes/charts/series.py deck_generation/dev/scripts/showcase_charts_series.py`.
   Session log; RAVC2 to base RD CC `2.0.0_SA_COO` with /seams verdicts.

<acceptance_criteria>
- catalog shows your line/area/matrix chart archetypes under `Charts`.
- showcase_charts_series.py prints GATE PASS, 0 lint, full coverage.
- **/seams PASS on all 3 axes per chart** — verdicts in your RAVC2.
- Native charts editable; heatmap diverging maps monotonically; treemap areas proportional.
- Committed under your ~D author line on the DECK lane.
</acceptance_criteria>

<compiler_tools_mandate>N/A comp-* (deck tooling). Mandated validation = the **/seams** 3-axis pass per chart + design_lint [AUTO] (incl. chart-series A1) + COM visual-QA.</compiler_tools_mandate>
<cross_domain_coordination>`_native.py` shared (base-owned) — call, don't edit. You own `series.py`. Pull before commit. Base RD integrates.</cross_domain_coordination>
