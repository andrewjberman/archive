# ETFS_RIVALS -- reader census of gold `security_market` (G4), for PRD v0.19 G.4 / C-OWED-GRAIN

**By:** `2.0.0_SA_COO~RV`, 2026-10-07 ~21:3xZ, at CLOUD f9f8334ef6. **Method:** a read-only search agent swept the 41
product `.py` files under `data/etfs/scripts/rivalfunds` (tests aside) for the table name, the helper names and every
`.list(` call site, and opened 11; this seat then read the three deciding helpers itself (marked SEAT-READ) and listed the
live objects. No code was run against the table. Call-site lines not marked SEAT-READ are the agent's and are cited so a
reader can open them.

## THE ANSWER G.4 ASKS FOR

**No product reader takes all objects of a date. Every reader of G4 rows takes ONE object per date: the newest by the
capture time in the object's name.** So by G.4, "that reader is repaired first": no year of closes is written, by the
one-time load or by a top-up, until the readers take every object of a date (or the top-up is designed so that one
object per date is the whole truth).

What a second object on a date does today:
- A top-up whose name carries a LATER capture time than the base object REPLACES the base for that date in every reader:
  the date's live rows vanish from the rankings, the trend, the input census, the charts, the marker keys and the
  parsekey map. In the rankings stage `drop_backfill` then drops the top-up's rows as well, leaving the date EMPTY.
- A top-up with an EARLIER time, or a name with no time, is ignored.
- Nothing double-counts: no reader concatenates two objects of a date and every row reducer is keyed.

## The helpers that decide

| helper | rule | read |
|---|---|---|
| `gold_holding_contribution._newest_by_date` (lines 696-702) | groups every `.parquet` under the prefix by `date=`, returns `revision.newest(...)` per date: ONE uri per date | SEAT-READ |
| `revision.newest` / `order_key` (lines 101-118) | max over (partition date, live over import, capture time from the name, build sequence, legacy date, rebuild number, name) | SEAT-READ |
| `gold_holding_contribution._read` (lines 705-711) | one frame per date, concatenated ACROSS dates only | SEAT-READ |
| `gold_canonical_shape._g4_for` (620-651) | ONE date (the greatest at or before the report date holding a non-backfill row) and ONE object of it; an all-backfill object is never a candidate | agent |
| `gold_trade_schedule.load_parsekeys` (928-950) | one newest object per date over the frame's report dates | agent |
| `enrichment_bloomberg._stored_currencies` (747-771) | ALL `market-*` objects of each date, newest first, first non-backfill currency wins | agent |
| `enrichment_bloomberg._held_dates` (723-730) | existence of any `market-*` object marks the date held | agent |
| `publish_page._objects_in` (277-283) | ALL object NAMES in a window (no rows) | agent |

## Reader call sites (9 files read G4; 1 writes it)

| call site | objects per date | dates | use |
|---|---|---|---|
| `gold_holding_contribution.py:749-752` | ONE newest, then `drop_backfill` | window to the page day | prices, total return, GICS, names, parsekey for the rankings |
| `gold_buying_trend.py:306, 313` | ONE newest | window to the page day | parsekey join, display name |
| `gold_input_census.py:129-157` | ONE newest | window; and the as-of date alone | sector, parsekey; arrived / missing per holding |
| `gold_canonical_shape.py:863` via `_g4_for` | ONE newest live | one date per report date | GICS join onto G1 |
| `gold_trade_schedule.py:1043` via `load_parsekeys` (also `gold_flow_reconciliation.py:104`, `sweep.py:306`) | ONE newest | the frame's report dates | CUSIP / ISIN to Bloomberg key |
| `price_series.py:155-157` (called by `publish_page.py:723`) | ONE newest | 365 days to the as-of day | **the chart's closes**, currency, parsekey -- SEAT-READ |
| `publish_page.py:674-676` | ONE newest | window to the page day | parsekey for marker keys |
| `publish_page.py:295` `_a1_newer_input` | ALL names | the A1 window | staleness trigger for the A1 rebuilds |
| `enrichment_bloomberg.py:804, 807` | existence; ALL `market-*` | the backfill's range | skip held dates; stored currency |

Writer: `enrichment_bloomberg.py` only, as `market-<capture time>-<digest>.parquet`; its three modes (daily pull, import,
`market-range` backfill) each refuse to overwrite a name; `market-range` writes only dates that hold no `market-*` object
and marks every row `as_of_source = "backfill"`.

Outside the product: `data/assets/scripts/analysis/commonwealth_price_census.py:64, 396-440` reads ALL objects of ALL
dates and de-duplicates. Whether anything schedules it was not checked.

## The live table (listed 21:3xZ by this seat): 8 objects over 5 dates

| date | objects |
|---|---|
| 2026-09-29 | 2 (`market-20260929-53bc...` 29,661 B; `market-20260929-afcd...` 11,511 B; neither name carries a time) |
| 2026-10-01 | 1 |
| 2026-10-02 | 3 (11:05Z 10-04, 46,943 B; 12:33Z 10-05, 19,670 B; 12:46Z 10-05, 46,943 B) |
| 2026-10-05 | 1 |
| 2026-10-06 | 1 |

So the one-object rule already decides today on two dates. On 2026-10-02 the winner is the 12:46Z object; the 19,670 B
object of 12:33Z is ignored. What rows the ignored objects hold that the winner lacks was NOT read.

## What follows for the cut of FWD-24 (issuer's reading; the design is the PRD's)

1. The readers' grain is one object per date at 6 row-reading call sites through 3 helpers. Repairing "the reader" is
   one change in `_newest_by_date` / `_g4_for` / `load_parsekeys` (take every object of the date, one row per
   security and date by a stated precedence: live over backfill, newer capture over older), not six.
2. `market-range` cannot be the top-up writer as it stands: `_held_dates` skips any date that already holds an object,
   which is every date the daily leg has written.
3. A G4 object newer than an A1 table triggers a rebuild of holding_contribution and input_census but NOT buying_trend
   (`publish_page._a1_window` returns None for it, though the trend stage reads G4).
4. Also seen: `_held_dates` and `_stored_currencies` see only names starting `market-`; the product readers accept any
   `.parquet`. A top-up must keep the `market-` name form or it is invisible to the backfill's own logic.

## Not determined

- What the two ignored live objects contain.
- Whether the tools `tools/g5_drift.py` and `tools/g5_code_replay.py` ever see G4 in their local scratch.
- Whether anything under `integrations/` writes G4 by another path (the table's name does not appear there).
