# ETFS_INGEST.TO-5 — acceptance record (`INGEST-T5-1`, `INGEST-T5-2`)

**Seat:** `0.4.0_DE_ClientPlatform~Z` · **Date:** 2026-08-24 · **TO** @`efa80f37a4` · **Decomp** @`fcdf042972` (CERTIFIED)
**Portal vintage for every claim:** `d43b88c5` (= `origin/DEV`), branch `DEV`, tree clean.
**Baseline evidence:** `deZ_ETFS_INGEST_Z-S12_RENDER_READ_20260824.md` @`b332cc4fa2`.

⛔ **NO PORTAL FILE WAS EDITED.** This TO's executable half (`AC4`) is gated on a field that is not pulled, and `AC6` resolves to option **(b)** — a determination, not a build. Everything below is measurement + a ruling-grade recommendation.

---

## `INGEST-TO5-AC1` — DISCHARGED AT ISSUANCE

Rendered under CTO~Z's direction before the TO arrived. Verdict: **labels correct, colour channel dead — it renders UNDIFFERENTIATED, not wrong.** Full read in the baseline record. Not re-run, per the TO.

---

## `INGEST-TO5-AC2` — the census, with denominators, and the ETF-only/SHARED split

**Instrument 1 — token census** (case-insensitive per Rule 21), denominator **10 files** in `src/pages/Positioning/` + the two shared lookup homes:

| file | `sub_asset_class`/`subAssetClass` hits |
|---|---|
| `Positioning/tabs/HoldingsTab.tsx` | 27 |
| `Attribution/constants/holdings-shared.tsx` | 17 |
| `Positioning/shared/etfAdapter.ts` | 2 |
| `Positioning/panels/PositioningSummary.tsx` | 2 |
| `lib/chartColors.ts` | **0** |
| the other 7 in-tree files | 0 |

⚠ **THE FLOOR BIT IMMEDIATELY, EXACTLY AS `AC2` WARNS.** `chartColors.ts` reads **0** for the token yet **defines `SUB_ASSET_COLORS`, one of the three tables under investigation.** A token census cannot see a constant whose *keys* are the vocabulary. **The token count is not the site list**, which is why the structural pass below is the load-bearing instrument, not the corroborating one.

**Instrument 2 — structural pass** (symbol importers = actual blast radius):

| symbol | importers | ETF-only or SHARED |
|---|---|---|
| `SUB_ASSET_CLASS_COLORS` | `holdings-shared.tsx`, `HoldingsTab.tsx` | **SHARED** (Attribution + Positioning) |
| `SUB_ASSET_COLORS` | `chartColors.ts`, `HoldingsTab.tsx` | **SHARED** (lib) |
| `ASSET_CLASS_COLORS` | `holdings-shared.tsx`, `HoldingsTab.tsx`, + **3 Attribution components** | **SHARED** |
| `getAssetClassBgColor` | `holdings-shared.tsx`, `HoldingsTab.tsx`, **`Attribution/tabs/SelectionTab.tsx`** | **SHARED** |

> ⛔ **THE FINDING: THERE ARE ZERO ETF-MODE-ONLY LOOKUP SITES. EVERY ONE IS SHARED** — with Models mode (same `HoldingsTab` component, both modes) *and* with the Attribution page. So any table edit is an `AC3` event by construction, and its blast radius reaches a **second page** the TO does not mention.

---

## `INGEST-TO5-AC3` — Models byte-identical

**No portal file was edited, so Models mode is byte-identical trivially — the strongest possible form, and it is not a claim I had to test.** Recorded rather than asserted: the criterion is satisfied by the absence of a diff, which `git status --porcelain portal` = 0 lines confirms.

⚠ **STATED FOR WHOEVER BUILDS `AC6` OPTION (a):** it would *not* be trivial there, and the reason is not the colours. `SUB_ASSET_CLASS_COLORS` **membership is a control-flow branch**, not just a palette lookup — `getSubAssetClass` (`holdings-shared.tsx:136-148`) returns the normalized value **only if `SUB_ASSET_CLASS_COLORS[normalized]` exists**, else falls through to `getETFCategory(ticker)`. **Adding keys changes which branch Attribution's `SelectionTab` takes for existing Models holdings.** That is an AC3 regression path through a page nobody is watching.

---

## `INGEST-TO5-AC4` — **KNOWN-UNREACHABLE**, declared not left open

The field is not pulled, measured on the **applied** plane (the landed artifact), not only source:

```
bbg/2026-08-21/characteristics.csv header:
security,NAME,EQY_DVD_YLD_IND_NET,BETA_ADJ_OVERRIDABLE,GICS_SECTOR_NAME,
CNTRY_OF_DOMICILE,CUR_MKT_CAP,FUND_EXPENSE_RATIO,FUND_TOTAL_ASSETS,
TOTAL_NUMBER_OF_HOLDINGS_IN_PORT,TRACKING_ERROR

GICS_INDUSTRY_GROUP_NAME : 0     <- the gate
GICS_SECTOR_NAME         : 1     <- POSITIVE CONTROL, fired
```

The other half of the side-by-side **is** landing: `bbg/2026-08-21/constituents/derived_sector_allocation.csv` carries `sector_name` = `Health Care (Equity)`, `Energy (Equity)`, … per fund. **So `AC4` is blocked on one of its two inputs, not both.** Unblocks when `INGEST-T3-6` carries the field into the gold row (DS-class, A2-sequenced).

---

## `INGEST-TO5-AC5` — the overlap re-check, handed off BY SERIAL — **and the premise is half what it was stated as**

**Hand-off:** `0.4.0_DS_ClientPlatform~Z` owns the `etf_daily_pull.py:141` field-list edit when the additive field lands, and **owns the re-check at that edit.** The two fast-moving fields: **`TOTAL_NUMBER_OF_HOLDINGS_IN_PORT`** and **`FUND_PCT_TOP_TEN_HOLD`**.

⚠ **RE-DERIVED, AND IT DISAGREES WITH THE TO'S PREMISE — MINE GOVERNS AND I AM ROUTING IT, NOT EDITING IT.** The TO (carrying MSTR~Z's measurement) describes both fields as *"`characteristics`' fast-moving members … independently captured by the constituents leg"* — i.e. an overlap of two. Measured on the 2026-08-21 landed files:

| field | in `characteristics.csv` | in `constituents/derived_summary.csv` | so it is… |
|---|---|---|---|
| `TOTAL_NUMBER_OF_HOLDINGS_IN_PORT` | **yes** | **yes** (`total_number_of_holdings_in_port`) | a genuine overlap |
| `FUND_PCT_TOP_TEN_HOLD` | **NO** | **yes** (`fund_pct_top_ten_hold`) | **SOLE-SOURCED to the constituents leg** |

> **The overlap is ONE field, not two — and for the second the dependency runs the OTHER WAY.** `FUND_PCT_TOP_TEN_HOLD` has no `characteristics` copy to fall back on, so a constituents-leg failure loses it outright. **A premise offered as reassurance ("survivable") is, for half its members, the opposite.** Bound: one as-of (`2026-08-21`), and `etf_daily_pull.py:141` is one of at least two field lists (the landed header carries members that line does not), so **which list requests `FUND_PCT_TOP_TEN_HOLD` is UNMEASURED** — I did not trace it, and it is DS~Z's file.

---

## `INGEST-TO5-AC6` — **DETERMINATION: OPTION (b).** Colour is deliberately NOT carried at the 24-value grain

The TO permits either (a) cover the values across the tables with a Rule-24 record, or (b) state with the render as evidence that colour is not carried at this grain **and what replaces it**. I determine **(b)**, on four independent legs.

### Leg 1 — 24 values is 3× the categorical-colour ceiling, and the estate is already past it

Categorical colour has a hard ceiling around **8 slots**; beyond it a 9th series is never a generated hue — it folds into "Other", small multiples, or composite encoding. Measured against the estate's own table:

| | count |
|---|---|
| categorical ceiling | **8** |
| `SUB_ASSET_CLASS_COLORS` distinct colours today (21 keys) | **16** — already 2× |
| today's live ETF vocabulary | 11 — already above 8 |
| C3's `GICS_INDUSTRY_GROUP_NAME` | **24** — 3× |

**So option (a) cannot be done correctly at 24 values.** Covering them means inventing 24 distinguishable hues, which the colour rules forbid *and* perception does not support. Note this also means **"fix the 0-of-11 miss by adding 11 keys" is not a clean fallback** — 11 is above the ceiling too.

### Leg 2 — option (a) touches FOUR sites, and the fourth is a silent contrast defect

The TO names three tables. **There is a fourth, and it is the one that bites.** `getSubAssetTextColor` (`chartColors.ts:307-313`) picks text colour from an **8-entry allowlist** of light backgrounds:

```ts
const lightBackgrounds: string[] = [
  PALETTE.white, PALETTE.green100, PALETTE.green200, PALETTE.green400,
  PALETTE.blue100, PALETTE.blue200, PALETTE.blue300, PALETTE.blue400,
]
return lightBackgrounds.includes(bgHex) ? PALETTE.gray900 : PALETTE.white
```

**Any new colour not added to that list silently gets WHITE text.** A light new hue therefore ships white-on-light — the estate's #1 recurring portal defect, invisible to a grep and to typecheck, visible only in a render. Four sites: `holdings-shared.tsx:71`, `chartColors.ts:279`, `HoldingsTab.tsx:136`, **`chartColors.ts:307`**.

### Leg 3 — the estate has ALREADY made this exact decision, on another page (build ladder rung 2)

`industryGroup` is **live today** in SecurityScanner (`SecurityScanner/types.ts:75`, `// source: indgrp_name`) and PortfolioManagement — 9 occurrences. How it is encoded (`UniverseDataTab.tsx:150-156`):

```ts
{ field: 'industryGroup', headerName: 'Industry Group',
  minWidth: 200, filter: 'agTextColumnFilter',
  cellStyle: { opacity: 0.7 } }
```

**Plain recessive text, a text filter as the discriminating interaction, a wider column than Sector (200 vs 160), and NO colour.** Census: **0** occurrences of any colour keyed on `industryGroup` anywhere in `src`. **The estate colours nothing by industry group, and it already renders the exact vocabulary C3 ruled.** Option (b) is not a new position — it is the existing one, and choosing (a) would make Positioning the only page that disagrees with it.

### Leg 4 — I tested my own remedy in a render, and it FAILED in its naive form

I proposed text as the replacement channel, then rendered a **synthetic** 24-value fixture to test that proposal rather than assert it — `deZ_ETFS_INGEST_T5_render_SYNTHETIC-24value-labelfit_20260824.png`.

⛔ **THE LABELS OVERFLOW THE COLUMN AND COLLIDE WITH THE TICKER COLUMN.** Visible collisions: `Technology Hardware & Equipm`+`AAPL`, `Semiconductors & Semiconducto`+`MSFT`, `Health Care Equipment & Servi`+`JNJ`, `Pharmaceuticals, Biotechnology & Life Scienc`+`ABBV`, `Commercial & Professional Serv`+`CMI`.

Source-confirmed cause — `HoldingsTab.tsx:1160-1162`:

```tsx
<col style={{ width: '105px', minWidth: '105px' }} /> {/* Asset Class */}
<col style={{ width: '165px', minWidth: '165px' }} /> {/* Sub Asset Class */}
<col style={{ width: '55px',  minWidth: '55px'  }} /> {/* Ticker */}
```

**165px, fixed, sized for the Models vocabulary** (`Intermediate`, `US Large Cap` — ≤21 chars). The longest GICS industry group is **46 chars** (`Pharmaceuticals, Biotechnology & Life Sciences`). SecurityScanner uses **200px** for this same vocabulary and is itself likely tight.

> **So T5-1 has a THIRD component nobody had named: COLUMN GEOMETRY.** Field swap + colour determination + **the table has to be re-measured for the longer vocabulary.** Had option (b) shipped as "just render the text", it would have shipped a collision.

### The determination, stated for the record

**Colour is deliberately NOT carried at the `GICS_INDUSTRY_GROUP_NAME` grain.** What replaces it as the discriminating dimension:

1. **The text label itself** — already proven correct by the AC1 render (the fallback returns the raw value), **conditional on the column being widened** per Leg 4.
2. **Sort / grouping order** — adjacency does the categorical work colour cannot at 24 values.
3. **A text filter**, matching SecurityScanner's existing pattern for this exact vocabulary.
4. **Colour stays at the `asset_class` grain** (`Equity` / `Fixed Income` / `Cash` = 3 values, comfortably within the ceiling) — **which is precisely what `getAssetClassBgColor`'s fallback already does today.**

> ⛔ **THE SHARPEST FORM OF THIS FINDING: THE CURRENT BEHAVIOUR IS WHAT THE COLOUR RULES WOULD PRESCRIBE ANYWAY. The defect was never that it falls through — it is that it falls through UNDECLARED, so nobody could tell a decision from an accident.** `AC6` is discharged by *declaring* it, not by changing it. That converts a dead channel into a stated design position, which is exactly what the criterion asks for and is why (b) is the cheaper *and* the more correct answer.

⚠ **BOUND ON THE SYNTHETIC FIXTURE.** `deZ_ETFS_INGEST_T5_SYNTHETIC_24value_fixture_20260824.json` uses **real, published GICS industry-group names** mapped deterministically from each holding's real sector, purely to test **render geometry**. **It is NOT a data claim, no such field is pulled today, and it must never be cited as one.** What it demonstrates (label fit) is a property of the layout, not of the data.

---

## `INGEST-TO5-AC7` — screenshots landed durably

| artifact | what it shows |
|---|---|
| `deZ_ETFS_INGEST_T5_render_models-empty_20260824.png` | Models mode, empty backend — the render that proved the site-Z toolchain |
| `deZ_ETFS_INGEST_T5_render_etfs-today_20260824.png` | ETF mode **today** — flip works, cause-agnostic unavailable notice |
| `deZ_ETFS_INGEST_T5_render_etfs-fixtured_20260824.png` | ETF mode with the **real** artifact — the `Z-S12` answer |
| `deZ_ETFS_INGEST_T5_render_SYNTHETIC-24value-labelfit_20260824.png` | **SYNTHETIC** — the Leg-4 column-collision evidence |

All under `org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/`, committed. First three @`b332cc4fa2`.

---

## Surprise items routed (OBSERVATION — none interrupt)

1. **The `getSubAssetTextColor` allowlist (4th site)** — a new colour omitted from it ships white-on-light silently. INERT today (nobody is adding colours); becomes live the moment anyone attempts option (a). Disarm owner would be whoever takes (a) — **nobody, under this determination.**
2. **`AC5`'s half-overlap** — `FUND_PCT_TOP_TEN_HOLD` is sole-sourced to the constituents leg, and the record says otherwise. Routed to `0.4.0_DS_ClientPlatform~Z` at the field-list edit.
3. **`SUB_ASSET_CLASS_COLORS` membership is control flow**, not just palette — an Attribution regression path.
4. **Column geometry (165px)** is a third T5-1 component.

## Declared exclusions

- **The promote** — Andrew's word, not this TO's.
- **Any portal edit** — `AC4` gated, `AC6` resolves to a determination; nothing to build this turn.
- **Whether the Models artifact's vocabulary can reach the tables** — I could not locate a Models `positioning_data.json` under `opal-data-portal-v2/platinum/` (only `advi/ etfs/ mdpf/`) or `opal-data-assets/json/`. **UNMEASURED, named rather than assumed**; not load-bearing for this determination, which rests on the tables and the render.
