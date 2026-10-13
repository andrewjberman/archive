# MDPF_CANON FWD-9 -- the AUA Trend grouping: read before the cut (fork of 2.0.0_SA_COO~D1, 2026-10-13 ~19:3xZ)

Read-only. Input: CTO msg 5067, PRD v2.12 FWD-9, Andrew's record. Anchors are file:line at HEAD; served objects read 2026-10-13 (global `aggregate-aua-timeseries/2026-10-12.json`, `category-views/2026-10-12.json`). Nothing here is a cell, an order or a commit.

## 1. The requirement

- PRD `org/missions/D8/MDPF/MDPF_CANON/prd/MDPF_CANON_PRD.md:188-204` (FWD-9): on Model Portfolios > AUA TREND ANALYSIS > Trend (period-end bars, daily area chart, legend): every custom model summed into ONE series "Custom Models" in the colour the Total Assets "Models" card hover uses for custom models; ALT Strategies, ETF Strategies, Client Supervised and Client Unsupervised each ONE series with its own legend chip in the Total Assets grouping and colours; the canonical Opal models stay as their own series; each grouped series equals the sum of its members on three drawn dates. Negative arm: "today's build lists about 17 individual series".
- L10 addendum `:510-526`: "No new color and no new data are needed; the sums are of series the page already serves"; grouping server-side if the served payload is what the chart iterates, else in the component, reusing the Total Assets grouping function; client-facing, PROD push is Andrew's card.
- Andrew's words: `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261013_184xZ_MODEL_PORTFOLIOS_AUA_TREND_GROUP_CUSTOM_MODELS_AND_CHIPS.md` (his legend listed about 17 series).
- "Total Assets" = the `CategoryViewTree` card whose headline reads `Total Assets` (`portal/src/components/CategoryViewTree.tsx:1317`); "Models" card hover = the L1 bar of Models > Primary / Custom (`:320-361`, `:478`).

## 2. What draws the Trend today, and what the Total Assets card does

Trend (`portal/src/pages/ModelPortfolios.tsx`):
- Series are built CLIENT-SIDE from the served global `by_model` (`:782-856`): every key whose `cohort_class !== 'sma'`, named by `getCanonicalModelName(display_name)`; the 50/50 blends are rolled into the archetype models by `rollBlendsIntoArchetypeSeries` (`:855-858`). Order `trendModelOrder` = `orderModelsWithBlends(keys)` (`:864-867`); mount list `trendStackSeries` = fixed `STACK_SERIES` spine `:146-157` plus appended extras (`:888-896`).
- Bands beside the models: `Non-Model` (shown as "Other AUA"), `Additive SMA sleeves` (`sma_additive_aua`), `Tax-Managed SMA` (`tax_additive_aua`), Global only (`:1157-1161`, `:1904`, `:2106`).
- Legend: `renderTrendLegend` (`:1148-1170`); colours via `getModelColor` (`portal/src/lib/modelPortfolioColors.ts:18-209`; Tax-Managed SMA entry `:139-144`); tooltip `renderTrendTooltip` (~`:1076-1142`).
- Today's count on the served global object: 16 non-SMA `by_model` keys, 14 after the blend roll, + Non-Model + Additive SMA + Tax-Managed = **17 series** (Andrew's "about 17").

Total Assets card (`CategoryViewTree.tsx`): groups SERVER-SIDE. It renders the served `category-views.nodes` tree; the grouping is the tree's own children. Colours are client-side by name: `L1_COLOR` (`:87-95`): Primary `indigo400`, **Custom `fuchsia500`**, `ETF Strategies` `cyan400`, `ALT Strategies` `green400`, `Client - Opal Supervised` `amber400`, `Client - Opal Unsupervised` `orange500`; L0 (`:613-617`): Models `violet300`, SMA `teal500`, Client `amber400`. `L1_COLOR` and `l1ColorOf` are module-private (`const`, not exported).

A second, different palette exists: `ModelPortfolios.taxsma-color.test.ts:28` maps `'ETF Strategies': '#6366f1'`, so the trend's own SMA colours are not the Total Assets ones.

## 3. Mapping: where each group lives in served data, and its history

| group | served carrier | per date (history) | as-of only |
|---|---|---|---|
| Custom Models | `category-views` Models > Custom (12 members; `member_id` equals the ts `by_model` key); ts `by_model` custom keys (cohort_class `model`) | ts: all 495 dates | the Primary/Custom marker itself (the ts has no group field) |
| canonical models | ts `by_model` 5 core keys; Models > Primary | all dates | |
| ETF Strategies | category-views SMA > ETF Strategies: Dividend SMA `divz` (ts `opal_div_sma`), Opal Equity Growth SMA `pfoe` (ts `opal_growth_sma`), IDVZ, PFDE (ts `pfde`) | ts SMA-class lines, all dates | the group node |
| ALT Strategies | category-views SMA > ALT Strategies: Muni SMA, Tax-Managed SMA `tax` (ts `tax` and `tax_additive_aua`) | `tax_additive_aua` all dates | the group node |
| Client Supervised / Unsupervised | category-views Client > Opal Supervised 286,311,083.45 / Unsupervised 0.0 | **NOT in the ts** (no key carries them: "upervised" occurs 0 times in the global ts) | **only the 21 dated category-views objects (2026-08-27 .. 2026-10-12)** |

Denominators: ts dates 495; category-views dated objects 21; `non_model_assets_detail.time_series` rows 498, aggregate non-model only (no supervised split).

So the L10 addendum's "no new data are needed" holds for Custom Models, the canonical models, ETF and ALT, and does NOT hold for Client Supervised and Client Unsupervised: no per-date series of either exists in any served object.

## 4. Interplay with the CN-f-1 fold (deployed 2026-10-13, first folded fire 2026-10-14 13:30Z)

- The fold removes the 11 model-class lines held by fewer than two firms from the global `by_model` and emits ONE `other_models` line, only on dates held by two firms; those 11 lines are almost exactly the Custom members (the category-views Custom node at the as-of, $68.04M, sums them).
- After the first folded fire the global ts has 5 core lines + `other_models` as non-SMA `by_model` keys, so the Trend draws about **9 series** (5 core, Other Models, Other AUA, Additive SMA sleeves, Tax-Managed SMA). The "crowd of 17" is gone by the fold itself; what FWD-9 still adds is the NAME "Custom Models", the colour `fuchsia500` and the chips for ETF/ALT/Client.
- History: `other_models` is emitted on 47 of the 102 dates that carry a positive pooled total (suppressed 2026-05-15 .. 2026-09-09, inflection alone), and the per-model detail of the core lines begins 2026-05-15. The Custom Models series will therefore have a gap before roughly 2026-09-10, by accepted ruling.
- "Each grouped series equals the sum of its members on three drawn dates": after the fold the members are no longer served for the folded dates, so that arm can be read only against the PRE-fold object (the prior dated object keeps its one-firm lines) or against the fold's own invariant (other_models = the sum of the removed lines, graded by `r6_fold_readback.py` R5). The cut must say which.
- Colour: `Other Models` is not in `modelPortfolioColors.ts`; the crosswalk row gave it display name "Other Models", not "Custom Models".

## 5. Server-side or component: recommendation

**Component, reusing the Total Assets tree, with no new JSON key.** Reasons:
1. The ts carries no group marker; adding one is a new served key (a never-widen pair and the "no new key" posture of the fold rulings), when the membership already exists in the served `category-views` (`member_id` equals the ts key).
2. The Total Assets card already groups server-side (the tree) and colours by name; the cut reads the as-of category-views membership once and maps ts `by_model` keys to L1 groups (static by registry), summing per date. Build ladder step 2: reuse.
3. `L1_COLOR` / `l1ColorOf` must be exported from `CategoryViewTree.tsx` (one line) so the Trend uses the Total Assets colours, not a second palette.

Open and not decidable by the issuer: Client Supervised/Unsupervised have no per-date series. Options for the CTO: (a) chips only on the 21 dates that have a category-views object (a partial history, honest-absent elsewhere); (b) a producer change to emit a per-date series (a new served key, its own cell and pair); (c) chips at the as-of only (legend) with the bars unchanged. FWD-9 as written ("each ONE series") is met only by (a) or (b).

## 6. The cut, if the CTO rules

- Owned files (one worker, `LOCAL` for the code, client-facing for the push): `portal/src/pages/ModelPortfolios.tsx` (series assembly, legend, tooltip), `portal/src/components/CategoryViewTree.tsx` (export the two colour symbols, no logic change), a test file beside `ModelPortfolios.taxsma-color.test.ts`.
- Mechanical criteria shape (at most three): (1) the grouping function: for three dates, group value equals the sum of its members, and the series list is the 5 core + the five groups + the existing bands; (2) the legend and colour tokens equal `L1_COLOR` for Custom, ETF, ALT, Supervised, Unsupervised (a token read, not a hex literal); (3) the portal typecheck `bun run typecheck` (never bare `tsc --noEmit`). The judgment criterion is the rendered screenshot via `scripts/ui-smoke.mjs` (CANVAS `rgb(244, 246, 250)`), read against `DESIGN.md` clauses, per `portal/CLAUDE.md`.
- PROD class: Model Portfolios is open to partner firms, so CLIENT-FACING: the promote is Andrew's card, with the before/after, beside the FWD-3 `/portfolios` card; DEV lands without his word.
- Sequencing: it is independent of CN-h-1 (different files); the fold's first fire should be read first so the Trend is drawn from the folded objects.

## 7. Not read

The ui-smoke render itself (nothing was run); the `getModelColor` entries for individual custom models beyond the grep; whether the period-end bars share the daily chart's series list (`:1890-2240`, assumed by the shared `trendStackSeries`).
