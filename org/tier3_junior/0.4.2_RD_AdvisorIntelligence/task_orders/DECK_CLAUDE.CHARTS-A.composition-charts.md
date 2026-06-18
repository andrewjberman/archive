# TO DECK_CLAUDE.CHARTS-A — Composition charts (doughnut / pie)

<issued_to>0.4.2_RD_AdvisorIntelligence~A</issued_to>
<issued_by>0.4.2_RD_AdvisorIntelligence (base, deck-system owner) — Andrew-direct chart fan-out</issued_by>
<project>DECK_CLAUDE</project>
<status>complete</status>

## Objective
Port the portal's **composition charts** into the new Charts family — real, EDITABLE, on-brand
python-pptx charts. You own `deck_generation/engine/archetypes/charts/composition.py` exclusively
(stubbed + wired). Targets + data shapes are in `deck_generation/dev/docs/portal-chart-port-map.md`.

## Build these (native DOUGHNUT/PIE via the shared `_native.opal_chart`)
- **chart-donut** — Model Portfolios allocation donut (segments by model + Non-Model; center total label).
  Source: `portal/src/pages/ModelPortfolios.tsx` (the donut radial). `opal_chart(s,"doughnut",labels,[("AUA",vals)])`.
- **chart-pie** — a composition pie (e.g. AdvisorIntelligence DistributionTab by segment).
  Source: `portal/src/pages/AdvisorIntelligence/_shared/tabs/DistributionTab.tsx`. `opal_chart(s,"pie",...)`.
- **chart-donut-center** — the donut + a highlighted-segment center label (the MP selected-segment variant).

## Build protocol
1. **Read first:** `dev/docs/portal-chart-port-map.md` (your targets + data shapes), `DESIGN_BIBLE.md` (law),
   `engine/archetypes/charts/_native.py` (`opal_chart` — palette/chrome/F2 are handled for you), and the
   portal source files above (extract the real data shape + segment order). The composer cwd is `deck_generation`.
2. **Edit ONLY** `engine/archetypes/charts/composition.py` (+ your showcase script + home-folder log). Do
   NOT edit `_native.py` (shared, base-owned), `compose.py`, `registry.py`, or another agent's chart submodule.
3. **Native charts** via `opal_chart(s, "doughnut"/"pie", categories, series)` — fn signature `(s, <data>)`;
   the caller does `s = d.slide("<tag>"); C.eyebrow(s, title)`. A1 palette + Lato + clean chrome are applied
   by `_native`. **F2: plot ONLY supplied data** (the archetype takes a real data payload — never fabricate).
   For chart-donut-center, overlay a center label with `C.text` (donut hole).
4. **register()** each (`("chart-donut","archetypes.charts.chart_donut","(segments: N x (label,value))","...",2,8,"...")`,
   `family="Charts"`).
5. **Showcase** `dev/scripts/showcase_charts_composition.py` — one slide per chart with REAL Opal data
   (the actual MP/AdvisorIntelligence allocation numbers), `Deck()` + `d.finalize(out)` -> **GATE PASS 0 lint
   + full coverage**; no consecutive-repeat (D10).
6. **/seams completion gate (REQUIRED — Andrew-direct):** run `/seams` on EACH chart archetype, validating all
   three axes: **MECHANICAL** (it generates + the showcase renders without error — "it can be generated"),
   **DECLARATIVE** (registered + the catalog claim is true to the impl + the chart TYPE matches the named chart),
   **SEMANTIC** (the rendered chart accurately + VISIBLY plots the supplied data — slice sizes match the values,
   magnitudes/proportions correct, Opal palette — render-grounded). Each chart must PASS all 3. Fix + re-run until clean.
7. **Visual-QA:** render the showcase via PowerPoint COM + READ every slide. Confirm donut/pie segments are
   Opal-colored, legible, no clutter. Native charts must be genuinely editable (open .pptx, double-click -> data grid).
8. **Self-commit (DECK lane):** pull latest CLOUD, then `.tools/safe-commit.sh --author
   "0.4.2_RD_AdvisorIntelligence~A <0.4.2_RD_AdvisorIntelligence~A@opal.agent>" -m "...~A: DECK_CLAUDE --
   composition chart archetypes + /seams PASS ..." -- deck_generation/engine/archetypes/charts/composition.py
   deck_generation/dev/scripts/showcase_charts_composition.py`. Session log; RAVC2 to base RD CC `2.0.0_SA_COO`
   with the /seams verdicts.

<acceptance_criteria>
- `python -m engine.compose --catalog` shows a `Charts` family with your composition chart archetypes.
- showcase_charts_composition.py prints GATE PASS, 0 lint violations, full coverage.
- **/seams PASS on all 3 axes for each chart archetype** (mechanical/declarative/semantic) — verdicts in your RAVC2.
- Native charts are editable (double-click in PowerPoint surfaces the data grid).
- Committed under your ~A author line on the DECK lane.
</acceptance_criteria>

<compiler_tools_mandate>N/A comp-* (deck tooling). The mandated validation here is the **/seams** 3-axis pass per chart + the design_lint [AUTO] gate (incl. the new chart-series A1 check) + COM visual-QA.</compiler_tools_mandate>
<cross_domain_coordination>`_native.py` is SHARED (base-owned) — do not edit it; call it. You own `composition.py` exclusively. Pull before commit. Base RD integrates all chart submodules into one Charts showcase.</cross_domain_coordination>
