# AMGT-re-1 -- THE FOUR SHAPE GAPS, and the file + change that closes each

`0.9.0_WK_AMGT_RESAPP~10` on `AMGT_RESAPP.TO-AMGT-re-1`, worktree `C:/tmp/wk-amgt-6-1`,
workspace branch `wk-amgt_resapp-6-1`, portal branch `wk-amgt_resapp-5-8-portal`
(started from `e6057f26`, the previous cut's 20 files, none of which were rebuilt).

**Nothing the adjudicator said was already present was touched.** The persistent Lead Panel,
the three tabs, the header Print location, the Model tab's cut and the rehoming of its figures
all stand as they were; the diff is eleven modified portal files plus four new Python files.

---

## GAP 1 -- CROSSED CONTROLS, NOT A ONE-TO-ONE MAPPING

> *"Trending/Breakout are mapped one-to-one to Chatter/Price instead of crossed controls."*

| File | The change |
|---|---|
| `portal/src/pages/SecurityAnalysis/types.ts` | **DELETED** `LeadPanelMode = 'trending' \| 'breakout' \| 'starred'` and `axisForMode()`, which *were* the one-to-one mapping. **ADDED** `MovementControl` (`TRENDING\|BREAKOUT`) and `SubjectControl` (`CHATTER\|PRICE`) as two separate types, and `CrossedAxis = ` template-literal cross of the two, so the four combinations are produced by the type system rather than hand-listed. **ADDED** `AxisResolution`, which every ranked payload now carries. |
| `portal/src/pages/SecurityAnalysis/constants.ts` | **REPLACED** the single `MODE_OPTIONS` list with `MOVEMENT_OPTIONS` and `SUBJECT_OPTIONS` -- two option lists, rendered as two pickers -- plus `CROSS_COMBINATION_COUNT = MOVEMENT_OPTIONS.length * SUBJECT_OPTIONS.length`. The rankings cache key now takes **both** controls. |
| `portal/src/pages/SecurityAnalysis/hooks/useSecurityAnalysisState.ts` | **SPLIT** one `mode` state cell into `movement` and `subject`, two `useState` cells with two setters and no coupling between them. `starredOnly` became a separate boolean, so Starred is no longer a value that *excludes* picking an axis. |
| `portal/src/pages/SecurityAnalysis/components/LeadPanel.tsx` | **TWO `<Select>` controls**, labelled `Movement` and `Subject`, either changeable without the other. Panel subtitle renders the live combination (`Trending x Chatter`, ...). Added `ResolutionNote`, which renders the served-partition record so a fallback is visible on the page. |
| `portal/src/pages/SecurityAnalysis/hooks/useLeadPanelApi.ts` | `useLeadPanelRankings(movement, subject)` -- two arguments, no mode-to-axis function anywhere in the file. |
| `portal/src/api/endpoints/amgt-lead-panel.ts` | `crossedPath()` emits **two** path segments (`/rankings/<movement>/<subject>`). A single "mode" segment would be the collapsed mapping again. |
| `lib/research/api/scoped_amgt.py` | `CROSSED_AXES` is **built as the product** of `MOVEMENTS` and `SUBJECTS`, never typed out (Rule 24(i)). `resolve_axis()` is the one place a (movement, subject) pair becomes a partition identity. |

**Measured, and it is the honest half of this gap:** no producer has ever written a
`TRENDING_*` or `BREAKOUT_*` partition -- only `CHATTER#<date>` and `PRICE#<date>` exist
(42 rows). So two of the four combinations fall back to the subject-only partition **and say
so**, per combination, in the payload (`resolution: SUBJECT_ONLY_FALLBACK`,
`movement_basis: ABSENT`) and on the page. Deriving the movement dimension client-side would be
re-deriving a ranking at render time, which this cell's BLOCK forbids. Filed as row
`AMGT_RESAPP-Z-W10-S2` with the producer cell named as the disarm.

---

## GAP 2 -- THE READ ADAPTERS

> *"required `/api/scoped/amgt` adapters are not delivered."*

| File | The change |
|---|---|
| `lib/research/api/scoped_amgt.py` **(new, 600 lines)** | The server half. Eleven routes under `/api/scoped/amgt`, one `handler(event, context)`, and `scoped_amgt_route_table()` returning the route list **as data** so the two halves can be diffed rather than asserted. Reads: `Query(IndexName='axis-rank-index', axis_date = :ad, ScanIndexForward=True)` for the ranked list, `GetItem(axis_date, ticker)` for a point, `BatchGetItem` of point reads for the series, landed-JSON reads for the per-security bundles, and a delegation to `lib/research/watchlist/store.py` for the starred set. `HARVEST_METRICS_TABLE` with `opal-harvest-security-metrics` as the default -- the same knob and default `chatter_axis.py:67` and `watchlist/store.py:43` already use. |
| `lib/research/api/tests/test_scoped_amgt.py` **(new)** | 16 tests, all passing. The ranked-order test feeds **deliberately scrambled** rows and asserts they come back unchanged -- a test fed pre-sorted rows could not tell a pass-through from a sort. The fake table has **no `scan` method**, so a scan-then-rank regression raises rather than passing quietly. |
| `portal/src/api/endpoints/amgt-lead-panel.ts` | The client half, rewritten onto the crossed routes, plus `getRankTimeSeries()` and an exported `printPackPath()` so the render check can assert the real action hits the real path without re-typing the string. |

**The auth gate is the estate's own, and it fails closed.** `auth-validator-edge` verifies the
RS256 JWT and *injects* `X-Firm-Id`, overwriting whatever the client sent
(`docs/architecture/PORTAL_AUTHHARD_PRD.md:21`). `_firm_id()` is the **only** source of firm
identity in the adapter; an absent header is a 401, and the watchlist routes carry **no firm
segment and no firm body field**, so a client cannot name a firm at all. Proven by
`test_a_client_supplied_firm_in_the_body_cannot_name_the_partition`, which sends a foreign
`firm_id` in the body and asserts the edge header won.

**What is NOT delivered, stated rather than implied:** the API Gateway route and Lambda
declaration that mount `scoped_amgt.handler` live under `infra/aws/terraform/`, which is not in
this cell's `<paths>`. Until an infra cell lands them the routes 4xx at the edge and the page
renders its stated empty states. Filed as row `AMGT_RESAPP-Z-W10-S3`.

---

## GAP 3 -- STARRED FILTERS, IT DOES NOT RE-ORDER

> *"The StarredList iterates stored starred order, contrary to the report's producer-order filter claim."*

| File | The change |
|---|---|
| `portal/src/pages/SecurityAnalysis/components/StarredList.tsx` | **Rewritten as a filter.** It no longer takes `starredTickers: string[]` and map over it; it takes `rows: RankingRow[]` (the producer's array as the GSI Query returned it) plus a `Set` of starred tickers, and its entire ordering behaviour is `rows.filter(row => starredTickers.has(row.ticker))`. There is no `.sort()`, no comparator and no key function in the file. |
| same | **It does not render rows at all.** It hands the survivors to `RankedList`, the cell's one row renderer, so the starred view and the unfiltered view *cannot* drift into two orders -- they are the same code. |
| same | The **residual is named, not dropped**: a starred ticker the producer did not rank on the selected combination has no rank on that axis, so it is listed separately, alphabetically, under a heading that says the order is not a ranking. Hiding it would shrink the firm's saved set; giving it a position would invent a rank. |
| `portal/src/pages/SecurityAnalysis/components/LeadPanel.tsx` | Starred became a **toggle over the selected combination** rather than a third value of the axis picker, which is what makes it a filter in the UI and not a mode. |

---

## GAP 4 -- THE CHART IS OVER TIME

> *"RankedChart is ticker-indexed and has no time-series implementation despite the stated automatic second-day behavior."*

| File | The change |
|---|---|
| `portal/src/pages/SecurityAnalysis/components/RankedChart.tsx` | **`BarChart` with `dataKey="ticker"` on the X axis is gone.** It is a `LineChart` whose X axis is `as_of_date` and whose *series identity* is the ticker -- one `<Line>` per name. Y is `rank`, `reversed` so rank 1 is the top. The only transform is a **pivot** (points re-keyed by date) plus chronological ordering, which is the X axis, not a ranking. |
| `portal/src/pages/SecurityAnalysis/types.ts` | **ADDED** `RankTimePoint`, `TickerRankSeries` (carrying `point_count`) and `RankTimeSeriesSet`. |
| `lib/research/api/scoped_amgt.py` | `read_rank_series()` -- `window_dates()` produces the N consecutive `axis_date`s ending on the as-of date, and the read is a `BatchGetItem` of `(axis_date, ticker)` **point reads**, the same GetItem shape batched. No Scan, no Query over an unranked set, and `rank`/`score` are carried verbatim from whatever the producer wrote on each date. |
| `portal/src/pages/SecurityAnalysis/hooks/useLeadPanelApi.ts` | `useRankTimeSeries(movement, subject, tickers)`, where `tickers` is the **head** of the already-ordered ranked rows. |

**Why it starts working on day two by itself, mechanically:** AMGT-rd-5 writes a new `axis_date`
every day, and the series read asks for a 30-day window of them. The number of X positions with
data grows by one per daily run with **no code change and no flag** on either side. Today exactly
one `axis_date` has landed per subject, so each line is a single point -- and the component prints
the per-series `point_count` beside the legend so the reader sees that denominator rather than
inferring it from a flat line. A single point is the honest render of one day.

---

## THE RENDER CHECK -- deliverable (b)

`portal/src/pages/SecurityAnalysis/__rendercheck__/renderCheck.tsx` (rewritten) +
`run_render_check.mjs` (this folder, the runner).

The previous cut rendered fixture components and a hand-copied trigger button. That shape is gone.

* **The real route.** `renderRoute()` mounts a real `MemoryRouter` at the real path with the same
  two `<Route>` declarations `App.tsx:433-434` carries, each wrapped in the real `ProtectedRoute`,
  inside a real `QueryClientProvider` and the real `AuthContext`. Both declared paths are rendered:
  `/security-analysis` (where the two crossed controls are on screen) and
  `/security-analysis/BABA_US_Equity` (Security mode).
* **The real action.** `exercisePrintAction()` drives `requestPrintPack()` -- the exact function
  `PrintExportAction`'s own `onClick` awaits -- with `fetch` replaced by a recorder, and asserts the
  URL it issues equals `printPackPath()` and that the `Authorization` header went out. The transport
  is stubbed; the action is not, and no button is re-typed anywhere in the file.
* **The render is READ, not captured.** `readColourLaw()` walks the emitted markup keeping a
  container stack and reports every light-text / ghost-white element that is **not** inside a dark
  container, per `portal/CLAUDE.md`'s colour law. The dark-container markers are read from the
  components' own emitted classes, not from a colour word in a comment.
* **The reader has its own control.** `colourLawInstrumentControl()` runs the reader against a
  light-text span on the bare canvas (must find it) and the same span inside a dark Panel (must
  not), and the runner **fails** if it cannot discriminate. A zero-findings result from a reader
  that has not been shown to return non-zero is the always-passes shape this whole recut exists
  to remove.

**Measured result** (`rendercheck_report.json`, `rendercheck_route.html`, this folder):

```
ROUTE /security-analysis            real Print button: true | persistent Lead Panel: true
                                    tabs: Thesis, Peers, Coverage | Movement control: true
                                    Subject control: true | Model tab: false
ROUTE /security-analysis/BABA_US_Equity   same, Model tab: false
declared combinations: 4   rendered panel states: 16   DISTINCT combinations seen: 4
  Breakout x Chatter | Breakout x Price | Trending x Chatter | Trending x Price
chart is over time: true            chart ticker category axis: false
print URL matches: true             print Authorization sent: true   print error: null
COLOUR LAW: 828 elements scanned, 43 dark containers, 302 light-idiom elements,
            0 VIOLATIONS outside a dark container
INSTRUMENT CONTROL: broken-world findings 1, clean-world findings 0, discriminates true
RESULT: OK: render check clean
```

**What this instrument does not establish, stated rather than left to be discovered.** No DOM
implementation is installed in this portal (`jsdom`/`happy-dom` absent; `package.json` is outside
this cell's write grant), so there is no real pointer click, no effect and no measured layout --
and none is claimed. `recharts`' `ResponsiveContainer` measures its box in an effect, so the
chart's inner SVG is empty in a server render by construction; that is why the component also
emits a text legend with point counts, and that legend *is* in the markup this check reads. No
DynamoDB is reachable from a render, so every query resolves to its loading/empty state; the
ranked-read contract is proven instead by `lib/research/api/tests/`.

---

## SURPRISE ROWS FILED

| Row | Class / hazard | What it says |
|---|---|---|
| `AMGT_RESAPP-Z-W10-S1` | OBSERVATION / ARMED | AC3's own `git checkout -- types.ts` restores from the index, so run mid-work it deletes the cell's uncommitted recut of that file. It did, here, and was recovered. The safe ordering is to run AC3 **after** the commit, which is what this cell's AC3 row records. |
| `AMGT_RESAPP-Z-W10-S2` | OBSERVATION / ARMED | Four controls, two producer partitions. The cross is real end to end; the movement dimension has no data until a producer writes it, and the fallback is disclosed per combination rather than collapsed. |
| `AMGT_RESAPP-Z-W10-S3` | OBSERVATION / ARMED | The adapters are code-complete and client-wired, but the route declaration that mounts them is under `infra/aws/terraform/`, outside this cell's `<paths>`. |
| `AMGT_RESAPP-Z-W10-S4` | OBSERVATION / INERT | 6 of 27 files on this cell's surface carry non-ASCII, all landed by the previous cut, all in files the recut is told not to rebuild. Everything this cell wrote is ASCII-clean. |

## WHAT THIS CELL DOES NOT CLAIM

* **FWD-15 is NOT REALIZED.** This cell makes it REACHABLE. A person still has to open the page,
  read a ranked list and click through to a name, and no artifact of this cell's own can stand in
  for that.
* **No portal promote, no push, no DEV/PROD merge.** Andrew-direct 2026-09-11 ~15:0xZ. The work is
  committed on `wk-amgt_resapp-5-8-portal` and nowhere else.
* **AC6 is not self-graded.** It is recorded UNVERIFIABLE-BY-INSTRUMENT for `3.0.0_SA_CVO~Z`.
