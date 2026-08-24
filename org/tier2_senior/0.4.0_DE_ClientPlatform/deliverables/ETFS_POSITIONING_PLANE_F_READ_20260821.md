# ETFS_POSITIONING plane (f) -- pre-cell READ of the five hardcoded model-list sites

**Seat:** 0.4.0_DE_ClientPlatform - **2026-08-21** - **READ ONLY, NOTHING BUILT.**
Per Andrew-direct 19:3xZ (ETFS_POSITIONING priority) + 19:4xZ (*"the canonical execution project I mandated is followed explicitly"*) and CTO's checklist item 1: **no write to code ahead of a cell-derived TO.** This document is the read, recorded so the cell is executable on arrival.
My cell `D4_ETFPOS.TO-D4e` remains gated on TO-D4c artifacts + D1's TO-D1b registry.

---

## The denominator first

`comp-find "'UST'" portal/src` -> **29 hits across 415 files**, 11 in the definition band.

**Exactly five sit inside `pages/Positioning/`** -- plane (f), my cell. **Six more carry the identical literal OUTSIDE the plane** and are NOT this cell: `MaxDrawdownChart:16`, `RollingCaptureChart:18`, `RollingSharpeChart:18`, `Attribution/SelectionTab:130` and `:212`, `FactorTilts/SummaryMetricsTable:87`, `ModelPortfolios/PeersTab:75`.

*"Five sites" and "every hardcoded model list in the portal" are different populations, and the second is more than twice the first.* Stated so a later cell does not discover them as a surprise.

## The five, and they are NOT the same problem

The distinction that matters for the flip: **an ORDER array tolerates a changed member set; a MEMBERSHIP array does not; and a DENOMINATOR array fails silently.**

| # | site | what it is | flip risk |
|---|---|---|---|
| 1 | `shared/gridConfig.ts:26` `PORTFOLIO_ORDER` | order **+ identity** -- `PORTFOLIO_NAMES = PORTFOLIO_ORDER.map(displayModelName)`, so the grid's columns *are* this list | membership-carrying; its own comment says "stay the 5 real models" |
| 2 | `shared/customBlend.ts:25` `MODEL_IDS` | **POSITIONALLY COUPLED ACROSS FILES** | **highest** -- see below |
| 3 | `panels/PositioningSummary.tsx:168` `portfolios` | key lookup into `positioningData.portfolios[code]`, and it builds the `values` array #2 depends on | membership-carrying; the other half of #2's coupling |
| 4 | `tabs/HoldingsTab.tsx:648` `allPortfolios` | **AGG weight DENOMINATOR** | **silent** -- see below |
| 5 | `tabs/HoldingsTab.tsx:779` `allPortfolios` | same block, **duplicated in the same file** | **silent**, and divergence-prone |

### #2 + #3 -- a hard index coupling across two files

`customBlend.ts`'s own comment states it:

> *"generateSections in PositioningSummary builds each row's `values` array in exactly this order, so blendSeries below assumes `value[i]` corresponds to `MODEL_IDS[i]`."*

So the blend math depends on **positional correspondence between an array in one file and a list in another**. Change the member set or the order in one without the other and the blend **silently mis-attributes** -- correct-looking numbers against the wrong models. No type error, no runtime error. These two must move together or not at all.

### #4 + #5 -- a denominator with a zero-fallback, written twice

```
const totalAUM = allPortfolios.reduce((sum, code) => sum + (aumByModel[code] || 0), 0)
```

`totalAUM` is the normalisation denominator for every AGG holding weight. **The `|| 0` means a member missing from `aumByModel` contributes zero rather than erroring** -- so if the flip changes the real member set and this list does not follow, every AGG weight is computed over the wrong population and is **quietly wrong**. A denominator built from a stale membership list is the exact shape this estate keeps getting bitten by.

And the block is **duplicated at `:648` and `:779`**. A fix applied to one and not the other leaves two AGG paths disagreeing -- which would present as an intermittent weighting bug, not as a missed edit.

## What this means for the cell (stated, not built)

- The flip is **not** five identical string-list swaps. One is order+identity, two are a cross-file positional contract, two are a duplicated silent denominator.
- **Models mode byte-identical** (PRD s.11.1) is a real constraint on #2/#3: any refactor that changes the *order* of the values array breaks the blend even if Models membership is untouched.
- The `:648`/`:779` duplication should be resolved to one source before either is made mode-aware, or the flip inherits a divergence hazard rather than removing one.

## Compiler Tools

`comp-find "'UST'" portal/src` (denominator + band split, the five vs the six outside the plane). Source read of each of the five at `file:line`; no tool substitutes for reading the coupling comments, which is where #2 declares itself.

## State

**Landed LOCAL, rides integration** (push-state stated per CTO's ruling 65604). Read only -- no code, infra, or data touched.

-- 0.4.0_DE_ClientPlatform, 2026-08-21
