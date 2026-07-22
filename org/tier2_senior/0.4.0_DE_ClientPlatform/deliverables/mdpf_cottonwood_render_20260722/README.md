# COTTONWOOD RENDER — S-9 CONFIRMED BY EXERCISE, AND IT IS WORSE THAN THE CENSUS PREDICTED

**Run by:** `0.4.0_DE_ClientPlatform` · **GO:** CTO 154932Z (*"run it, it is carve-out 3 and `STACK_SERIES`
alone justifies it"*) · **Portal:** `08c6d8b2`, branch DEV · **Harness:** `portal/scripts/ui-smoke.mjs`
**Read-only:** no portal source modified (portal tracked tree clean at `08c6d8b2`), no artifact moved, no
producer run, nothing served. Fixture-driven against the local vite dev server.

---

## THE FINDING

**A Cottonwood model whose key is not in the FE's `STACK_SERIES` literal renders BOTH TREND CHARTS
COMPLETELY EMPTY — while the legend confidently names both models and the donut renders them at full
value.**

The census (S-9) predicted *"a legend swatch, a donut slice, and NO BAR — the trend silently totals less
than the donut."* **The reality is worse: it is not a partial under-read, it is a TOTAL BLANK.** Both
"PERIOD END SUMMARY" and "DAILY AUM ANALYSIS" render axes, date ticks, and a full legend — and plot
**nothing at all.**

## THE CONTROL — why this is the KEY and not my fixture

A blank chart is exactly what a malformed fixture produces, so the finding is worthless without a
discriminating control. **The two fixtures are byte-identical except for the model keys:**

| | `fixture_test.json` | `fixture_control.json` |
|---|---|---|
| dates | 427, `2024-11-01 → 2026-07-20` | **identical** |
| values | CG 187.08M / INC 99.72M ramp over last 60 dates | **identical** |
| `non_model_aua` | all `None` | **identical** |
| **model keys** | `cottonwood_opal_conservative_growth`, `cottonwood_opal_income` | `opal_intermediate`, `opal_short_term` |
| **RESULT** | **BOTH CHARTS BLANK** | **4 stacked bars $0–$300M + full stacked area** |

**The harness can draw. The fixture is well-formed. The ONLY variable is the model key.**
Both Cottonwood keys are the REAL ones — `build_cottonwood_mdpf_slice.py:101-104`, the two
`PENDING_RULING` keys that exist in no canonical table.

- `cottonwood_TEST_noncanonical_keys__BLANK_CHARTS.png` — the defect
- `cottonwood_CONTROL_canonical_keys__CHARTS_RENDER.png` — the control that discriminates

## WHY IT HAPPENS
`ModelPortfolios.tsx:142-151` `STACK_SERIES` is a **closed 7-entry literal**; `:1891`/`:2060` mount a
`<Bar>`/`<Area>` only for its members. The legend (`:939 trendModelOrder.map`) and the donut
(`:613 Object.values(by_model)`) are **data-driven**. The page even *computes and stores* the value
(`:1789-1794`, `keyForModel` minting `m_<slug>`) and then drops it because no series is mounted.
**Every guard on this page was built for the VALUE being absent. None was built for the SERIES being absent.**

---

## ALSO CONFIRMED VISUALLY IN THE SAME PASS

**1. FE finding 10 — `getModelColor` fallback collapses distinct models to ONE colour.** In the test
render both Cottonwood models are **the same blue**, in the donut and in the legend — two different
products, visually indistinguishable. The control renders them orange + green. `modelPortfolioColors.ts:113-118`.

**2. FE finding 3 — the un-fixed methodology twin is LIVE and self-contradictory on screen.** The footer
asserts *"Non-Model AUM = Total AUM (Opal-managed) − Black Diamond Model AUM"* while the donut centre on
the same screen reads **"Not yet tracked"** for that very Total. A formula stated in terms of a quantity
the page says it does not have.

**3. FE finding 9 — the AUA/AUM label contradiction is real and firm-wide.** Donut centre says
**"Total AUM"**; the tile immediately beside it says **"Total AUA"** — same firm, same panel, both renders.
Pre-existing; affects 49F and Inflection too, not just Cottonwood.

**4. CONFIRMED FIXED, and worth saying plainly:** the honest-None footer fix (`08c6d8b2`) **works**. It
correctly emits *"No custody history is tracked for this firm yet, so no values are rolled forward."*
rather than the old false *"Values rolled forward from last known data."* Source attribution also resolves
correctly to **Black Diamond Rebalancer** for Cottonwood.

---

## NOT COVERED
- **COUNT mode not rendered** — only Value. The `STACK_SERIES` defect is structural and mode-independent,
  but the count axis produced a P0 earlier today and deserves its own pass.
- **Benchmark and Peers tabs not rendered** (FE finding 6: both are firm-blind).
- **This is a DEV-harness fixture render — necessary, not sufficient.** It proves the FE behaviour given an
  artifact shape; it does not prove what the served build does. The hard gate remains a post-promote render
  against the real served build.
- The distribution panel shows a local-dev CORS notice, not a finding.

## CONSEQUENCE FOR THE PLAN
This is a **silent wrong number on a partner-facing page** — the class a type-check cannot see and a grep
cannot see. It is **gated behind D6** (the merge-vs-add canonical-key ruling reserved to Andrew): if
Cottonwood's models are MERGED onto canonical keys the charts populate; if they are ADDED as new keys,
`STACK_SERIES` must be derived from the data or every Cottonwood model renders blank. **The render does not
decide D6 — it prices the ADD branch, which until now looked free.**
