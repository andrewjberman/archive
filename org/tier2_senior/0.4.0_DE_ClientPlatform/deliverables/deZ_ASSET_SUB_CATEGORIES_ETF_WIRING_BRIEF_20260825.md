# Asset Sub-Categories (Positioning Summary) -- what the frontend has, and what the backend must send

**For:** the backend/producer team wiring Economy/Sector data for ETF mode
**From:** `0.4.0_DE_ClientPlatform~Z`, 2026-08-25
**Andrew-direct:** *"I need the backend team to figure it the fuck out on setting up the data for that."*

---

## THE ONE-LINE ANSWER

**The frontend rendering machinery is COMPLETE and PROVEN. The section is switched OFF in ETF mode
because it reads a MODELS-ONLY feed, and the ETF equivalent that now exists is not wired to it.**
Nothing about ordering, colour, vocabulary or layout needs building. **One data shape needs deciding.**

---

## 1. WHERE THIS LIVES

```
Positioning page -> "POSITIONING SUMMARY" panel -> section "Asset Sub-Categories"
  src/pages/Positioning/panels/PositioningSummary.tsx
    :357   segmentRows built here
    :516   section emitted as { sectionName: 'Asset Sub-Categories', rows: segmentRows }
```
It is the LAST section of the summary table, one row per sub-asset class, one column per book. In
Models mode it renders today. **In ETF mode the rows are absent -- not empty, absent.**

## 2. ⛔ WHY IT IS ABSENT FOR ETFs -- THE ACTUAL GATE

```ts
// shared/bookSet.ts:132
capabilitiesFor('etfs') -> { ..., attribution: false }

// PositioningSummary.tsx:554
useQuery({ queryKey: ['holdings-attribution'], enabled: caps.attribution })
```
**`attribution` is a MODELS-ONLY feed, keyed by MODEL CODE, with no ETF counterpart.** It is
deliberately DISABLED rather than fetched-and-ignored, so the rows do not appear at all instead of
appearing empty. That was the correct call when written and it is now the thing to change.

## 3. WHAT THE FRONTEND CONSUMES TODAY (the Models shape)

```
attributionData.portfolios[<bookCode>].qtd.holdings[]   (falls back to .ytd.holdings)
  each holding: { sub_asset_class?: string, weight?: number }
```
**The frontend AGGREGATES per-holding rows itself** -- it walks holdings, groups by
`sub_asset_class`, and sums `weight` per book. It does NOT receive a pre-aggregated map.

## 4. WHAT ALREADY EXISTS FOR ETFs, AND THE MISMATCH

The ETF artifact (`s3://opal-data-portal-v2/platinum/etfs/positioning_data.json`) carries:
```
portfolios[<code>].segment.sector     { "Information Technology": 39.28, "Financials": 13.53, ... }
portfolios[<code>].segment.geography  { "US": 99.64, "Other": 0.36, ... }
portfolios[<code>].holdings[]         { sub_asset_class, weight, ... }   <- per-holding rows
```
>> **THE MISMATCH IS AGGREGATION LEVEL, NOT VOCABULARY.** `segment.sector` is a PRE-AGGREGATED map;
the frontend's existing code path expects PER-HOLDING ROWS and does its own grouping. **Both are
present in the artifact today.** <<

**Two options, and this is the decision the backend team owns:**

| | Option A -- reuse per-holding rows | Option B -- serve the pre-aggregated map |
|---|---|---|
| Source | `portfolios[code].holdings[]` (already served) | `portfolios[code].segment.sector` (already served) |
| Producer work | **NONE** | none, already emitted |
| Frontend work | flip `attribution: true` for etfs + point the aggregator at ETF holdings | new small reader |
| Pro | identical code path to Models; one aggregation rule in one place | cheaper payload; producer owns the arithmetic |
| Con | frontend re-derives numbers the producer already computed | **two aggregation homes that can disagree** |

**My recommendation: OPTION A.** The producer already ships the rows, the frontend already knows how
to group them, and it keeps ONE aggregation rule rather than two that can silently drift. Option B
recreates the two-homes divergence class this estate keeps paying for.

## 5. ⚠ WHAT THE BACKEND MUST GET RIGHT EITHER WAY

**(a) SPELLING IS LOAD-BEARING, ORDER IS NOT.**
The frontend keys on the EXACT sector strings and re-sorts on read:
```
'Energy' 'Materials' 'Industrials' 'Consumer Discretionary' 'Consumer Staples' 'Health Care'
'Financials' 'Information Technology' 'Communication Services' 'Utilities' 'Real Estate'
```
A near-miss spelling (`Healthcare`, `Info Tech`, `Technology`) falls to the unmapped bucket and
renders **dark at the bottom** -- it does NOT error. **Emission order is irrelevant**: the frontend
sorts by economy code on read, so append wherever is convenient.

**(b) THE AXIS DOES NOT SUM TO THE BOOK, AND THAT IS DELIBERATE.**
`segment.sector` has no "Other" bucket by design -- an unclassifiable holding is ABSENT from the
axis rather than being given a category that looks deliberate. Measured 2026-08-25:
```
DIVZ 99.80   IDVZ 96.82   PFDE 100.01   PFOE 99.99
```
IDVZ's 3.18 shortfall is ICT + MER + RBGLD -- unresolved identifiers. **Whoever wires the display
must decide what the panel shows for that gap.** Rendering nothing silently understates the book.
**This is a display decision that needs making, not a producer bug.**

**(c) CASH / FIXED-INCOME MEMBERS ARE EXPECTED AND ALREADY HANDLED.**
`sectorSortKey` places `Cash` and `Ultra Short Duration` BEFORE all GICS sectors and calls Cash
*"a real, expected member of the column that is NOT a GICS sector"*. Send them; they sort correctly.

## 6. WHAT IS ALREADY BUILT AND NEEDS NOTHING (ETFS_POSITIONING.TO-6, shipped)

```
GICS_SECTOR_CODE        11-row name -> GICS code map, keyed on OUR data's spellings
DECLARED_SECTOR_AXIS    those names sorted into Yang's ECONOMY_ORDER
sectorSortKey()         economy-order position, offset into a band clear of both ordering tables
sectorRampColor()       light -> dark BLUE ramp across the declared axis
SECTOR_UNMAPPED_COLOR   #111827, the dark bucket for anything off-axis
```
Ordering matches Portfolio Management (`ECONOMY_ORDER`, PortfolioManagement/constants.ts:104), the
ramp is Andrew-approved, Industrials is off the Equity tone (`blue550 #3073f1`), and the unmapped
bucket is deliberately dark. **None of this needs revisiting.**

---

## THE ASK, IN ONE SENTENCE

**Decide Option A or B, then flip `attribution` on for ETF mode and point the existing aggregator at
the ETF source.** The rendering half is done and proven; only the data wiring is open.
