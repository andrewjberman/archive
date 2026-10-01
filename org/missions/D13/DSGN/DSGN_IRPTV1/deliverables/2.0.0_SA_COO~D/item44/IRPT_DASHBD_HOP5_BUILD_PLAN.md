# IRPT_DASHBD FWD-1 hop 5 -- build plan (pre-stage; no code until the seam exists)

Seat `2.0.0_SA_COO~D`, 2026-09-30 ~18:3xZ. Authority: CTO 103252 / 103261 (C-LEASE, ruling 6.7: under a live DSGN_IRPTV1
FAST lease this seat builds workstream F's items as closer-drive items reading FWD-1 and C-SEAM, graded by the CVO as
DSGN_IRPTV1 pins). PRD `org/missions/D9/IRPT/IRPT_DASHBD/prd/IRPT_DASHBD_PRD.md` v0.3 (@c812be9885; ENDPOINT unchanged since
@2cb022f549). This file is a plan, not a build: FWD-1's ACCEPT fails any hop fed by a fixture, and C-SEAM forbids a page-side
shape the contract does not state.

## 1. What hop 5 waits on (measured 18:2xZ)

| Seam piece | Owner / cell | State | What the page needs from it |
|---|---|---|---|
| `org/standards/IRPT_DASHBD_SERIES_CONTRACT.json` | B, `DB-b-2` (worker `0.9.0_WK_IRPT_DASHBD~1`) | order `pending`; the worker spawns when `DB-b-1` reports the gold landed | the required / optional key lists and one sentence per field |
| `series.json.gz` + `manifest.json` for thread account 0027265115 | B, `DB-b-2` (local `--upload` run) | not written | the real bytes behind the curve |
| the read route `irpt-49f-reporting-read-lambda` | B, `DB-b-4` (depends on DB-b-2) | not cut yet | the signed-in page's one fetch of each file |

Un-parks when all three exist. `DB-b-2`'s order already fixes the field names (below); the plan binds to them, and the pin test
binds to the contract FILE, so a rename in the contract fails the page's test instead of drifting silently.

## 2. The series fields the page reads (from DB-b-2's order; the contract file is the authority once it lands)

- `series.required`: `date`, `value`, `total_return_daily`, `return_basis`, `day_quality`, `external_flow`, `income`,
  `holdings_price_return`, `method_version`, `as_of`, `first_data_date`, `history_scope`, `drawdown_episodes`.
- `series.optional`: `class_value`, `class_weight`, `class_names` (absent in round 1: the page reads absence as "no class view yet").
- `manifest.required`: `account_id`, `firm`, `method_version`, `as_of`, `first_data_date`, `history_scope`, `coverage_summary`,
  `byte_sizes`, `built_at`, `publisher_version`.
- Per-day arrays share one length (`series.array_keys`); dates strictly increase (DB-2-AC1 grades both on the writer's side).

## 3. What gets built (write surface: `tabs/reporting/` and the new `dashboard/` only, C-LEASE)

1. `portal/src/pages/InvestorReporting/dashboard/seriesContract.ts` -- the two document types, the key lists mirrored from the
   contract; a read that REFUSES a document missing a required key or carrying arrays of unequal length (a named refusal on the
   page, never a partial curve).
2. `dashboard/windowMath.ts` -- pure: the window's total return is the geometric link of `total_return_daily` over the chosen
   days (C-METHOD); days whose `day_quality` is `NOT_MEASURABLE` break the link with a stated gap and are counted; a start before
   `first_data_date` is clipped and says so (C-HONESTY); no annualization under one year, since-inception annualized only past a
   year; nothing summed that the file does not serve.
3. `dashboard/coverageWords.ts` -- one plain sentence per member of each axis (PRD v0.2 ruling 12), the member lists read
   from the gold contract's own `enums` block (`org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json`). Its DRAFT
   (uncommitted in the shared tree at 18:4xZ, contract_version 0.1.0, schema_hash b5fa8e4e48bf60ab) declares:
   `history_scope` FULL, PARTIAL_HISTORY (no MISSING_HISTORY: that member is the topics view's, C-TOPICS); `day_quality`
   MEASURED, FLOW_UNRECONCILED, LARGE_FLOW, NOT_MEASURABLE, SOURCE_LAG; `return_basis` TWR, HOLDINGS_INCOME_FALLBACK,
   NOT_MEASURABLE; plus column reasons `holdings_price_return_reason` NO_HOLDINGS_ROW, HOLDINGS_NOT_OK and
   `fee_amount_reason` FEE_RAIL_UNUSED (the label already says "before advisory fees"; no sentence repeats it). The page reads
   whichever of these the SERIES contract carries per day. An unknown member reads as its words, never a code, and fails a pin
   test so the list cannot fall behind the contract. Buildable the tick the gold contract is COMMITTED (a draft can move).
4. `dashboard/DashboardPerformance.tsx` -- the cumulative total-return chart with the headline number, presets 1M / 3M / YTD /
   1Y / Since inception plus the custom date pair and a brush (ruling 6.8); the label "Total return, before advisory fees" with
   the method version and "GIPS-aligned methodology, not GIPS compliance" one hover down (C-LABEL, ruling 6.1); the coverage
   sentences where the number is; fallback days footnoted. Chart colours from `chartColors.ts`, navy ink on white (C-DESIGN).
5. `tabs/reporting/ReportingTab.tsx` -- the switch (C-SHADOW, ruling 6.9): for an account whose manifest serves, the page shows
   this figure INSTEAD of IRPT_BCKEND's `PerformanceHeadline` / `PerformanceChart`, never both on one page; otherwise the
   current figure, unchanged. The switch is per account and reads only the manifest's presence.

## 4. How it is proven (the closer-drive bar, plus FWD-1's own trace)

- Own tests: the contract pin (the page's key lists equal the contract file's, read from disk); `windowMath` against the
  three 20-day windows DB-2-AC2 links from the gold (same numbers, same days); `coverageWords` covering every declared member;
  the refusal on a malformed document.
- `bun run typecheck` AFTER the last file is written (the miss of item 42 is not repeated), eslint on the touched files.
- ONE real run, signed in, on DEV with the real read route and the real file (no fixture on any hop): open account 0027265115,
  change the dates, and print (a) the time from the first byte to the painted chart, beside the file's gz size, and (b) the
  number of network requests after a date change, which must be 0 (C-SERVE: the browser computes every window).
- The trace is Andrew's next-morning pick (FWD-1 ACCEPT); the CVO grades the pin after the fact.

## 5. Sizes and order

- Items 1-3: one tick each, all testable before the file is served except the contract pin (which needs the file).
- Item 4: two ticks. Item 5 plus the real run: one tick, after DB-b-4 is planned AND applied by `2.0.0_SA_COO~P`.
- Nothing here is cut as a task order while the FAST lease lives; under FULL, F's orders name only `tabs/reporting/` and
  `dashboard/` (C-LEASE), and the CTO's next DSGN_IRPTV1 lease arm excludes those two paths or holds (CVO L4-R condition).
