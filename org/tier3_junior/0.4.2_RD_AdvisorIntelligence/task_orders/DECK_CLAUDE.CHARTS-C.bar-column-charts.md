# TO DECK_CLAUDE.CHARTS-C — Bar / column charts (incl. waterfall)

<issued_to>0.4.2_RD_AdvisorIntelligence~C</issued_to>
<issued_by>0.4.2_RD_AdvisorIntelligence (base, deck-system owner) — Andrew-direct chart fan-out</issued_by>
<project>DECK_CLAUDE</project>
<status>staged</status>

## Objective
Port the portal's **bar / column** charts into the Charts family. You own
`deck_generation/engine/archetypes/charts/bar.py` exclusively (stubbed + wired). Targets + data
shapes in `deck_generation/dev/docs/portal-chart-port-map.md`.

## Build these
- **chart-column-cme** — CME 10-yr expected return + volatility per asset class (a COLUMN for return +
  LINE/markers for vol — a combo). Source: `portal/src/pages/CapitalMarketAssumptions/`. Native via
  `opal_chart(s,"column",...)` then add the vol as a second series (or a paired line); A1 palette.
- **chart-bar-diverging** — Factor Tilts exposures, signed +/- about a zero baseline. Source:
  `portal/src/pages/FactorTilts/`. Native `opal_chart(s,"bar",...)` with a zero baseline.
- **chart-column** — a clean grouped column (Valuation metric per asset, or Positioning weights). Source:
  `portal/src/pages/Valuation/` or `Positioning/`. Native `opal_chart(s,"column",...)`.
- **chart-waterfall** — Attribution contribution waterfall (floating bars: start -> +/- deltas -> total).
  Source: `portal/src/pages/Attribution/`. **SHAPE-BUILT** (python-pptx has no waterfall): floating
  rectangles via C primitives, up=navy / down=purple, connector lines, A1 palette only.

## Build protocol
1. **Read first:** `dev/docs/portal-chart-port-map.md`, `DESIGN_BIBLE.md`, `engine/archetypes/charts/_native.py`
   (`opal_chart`), the existing **stat-stacked** archetype (`engine/archetypes/stat/__init__.py`) as the
   shape-built pattern for the waterfall, and the portal source files above (real data shapes). cwd = `deck_generation`.
2. **Edit ONLY** `engine/archetypes/charts/bar.py` (+ showcase + log). Do NOT edit `_native.py`/`compose.py`/
   `registry.py`/another agent's submodule.
3. **Native** via `opal_chart`; **shape-built** (waterfall) via C primitives, A1 palette only, true rects,
   no white-on-white (B3). **F2: plot ONLY supplied data.** A diverging bar uses the zero baseline (positive
   navy / negative purple is acceptable, both A1).
4. **register()** each (`method="archetypes.charts.<func>"`, `family="Charts"`).
5. **Showcase** `dev/scripts/showcase_charts_bar.py` — one slide per chart, REAL Opal data (real CME
   expected-return/vol, real factor exposures, real attribution deltas) -> **GATE PASS 0 lint + full coverage**.
6. **/seams completion gate (REQUIRED — Andrew-direct):** `/seams` each chart on all 3 axes — MECHANICAL
   (generates + renders), DECLARATIVE (registered + claim true + chart TYPE matches), **SEMANTIC** (render-grounded:
   bar heights match the values + signs; the combo's return-vs-vol mapping is right; the waterfall cumulates
   correctly start->total; Opal palette). Each must PASS all 3.
7. **Visual-QA** via COM + READ every slide (the waterfall cumulation + the diverging baseline are highest-risk).
   Native charts editable (double-click -> data grid).
8. **Self-commit (DECK lane):** pull, `.tools/safe-commit.sh --author "0.4.2_RD_AdvisorIntelligence~C <...~C@opal.agent>"
   -m "...~C: DECK_CLAUDE -- bar/column chart archetypes + /seams PASS ..." --
   deck_generation/engine/archetypes/charts/bar.py deck_generation/dev/scripts/showcase_charts_bar.py`.
   Session log; RAVC2 to base RD CC `2.0.0_SA_COO` with /seams verdicts.

<acceptance_criteria>
- catalog shows your bar/column chart archetypes under `Charts`.
- showcase_charts_bar.py prints GATE PASS, 0 lint, full coverage.
- **/seams PASS on all 3 axes per chart** — verdicts in your RAVC2.
- Native charts editable; the waterfall cumulates correctly.
- Committed under your ~C author line on the DECK lane.
</acceptance_criteria>

<compiler_tools_mandate>N/A comp-* (deck tooling). Mandated validation = the **/seams** 3-axis pass per chart + design_lint [AUTO] (incl. chart-series A1) + COM visual-QA.</compiler_tools_mandate>
<cross_domain_coordination>`_native.py` shared (base-owned) — call, don't edit. You own `bar.py`. Pull before commit. Base RD integrates.</cross_domain_coordination>
