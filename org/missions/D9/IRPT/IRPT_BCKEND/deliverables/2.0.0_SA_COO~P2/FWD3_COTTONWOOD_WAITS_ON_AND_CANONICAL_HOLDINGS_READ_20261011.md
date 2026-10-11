# What FWD-3 waits on for Cottonwood, and a read of the canonical holdings store (CTO msg 4704) -- READ ONLY, counts only

**By:** `2.0.0_SA_COO~P2` (dell2), 2026-10-11 ~10:4xZ. No write, no build. No account id, balance or figure is in this file.

## 1. What rows S250 and S252 say

Both are in `org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md`, surfaced 2026-10-01T12:22Z, both
still UNDER_INVESTIGATION, OBSERVATION, INERT.

- **IRPT_BCKEND-S250 is NOT about Cottonwood.** It is Inflection's: the coerced positions file for 2026-07-02 differs from its raw
  file in 4 of 59 columns on 9 of 33,618 rows, attribute columns only; nobody has read why; 2026-07-01 is not admitted and stays a gap.
  This seat's status file listed it beside S252 as a pair ("before either firm's holdings gold is served"); only S252 is Cottonwood's.
- **IRPT_BCKEND-S252 is Cottonwood's.** The Black Diamond holdings partitions hold their own date's close for most securities, but a
  minority carry the PRIOR day's close. Measured on 10 of 81 partitions: on five of the ten days, 3.4 to 5.9 percent of the securities
  that moved (18 of 526 to 22 of 371) are priced one day late. Not measured: which securities, and the other 71 partitions. The
  declared basis in `data/assets/scripts/gold/irpt_holdings_performance/sources.json` is one close per partition, `OWN_DATE`, basis
  `inferred`.

So, by these two rows, **what FWD-3 waits on for Cottonwood is S252 alone**: either the lagged minority is identified and handled, or
the basis is declared with that minority stated. The holdings gold must not be served on a date basis that has not been measured and
declared (PRD ruling 20).

## 2. The store the declared source reads is NOT the canonical store

Two different Cottonwood holdings stores exist, and S252 was measured on the first:

| | declared IRPT source | the store msg 4704 names |
|---|---|---|
| where | `opal-data-assets`, `blackdiamond/<scope>/silver/fact_holdings/date=YYYY-MM-DD/` (`sources.json`, entry `blackdiamond_z09`) | `s3://opal-data-cot/gold/canonical/holdings/{date}.parquet` (`infra/logic/registry/legacy_addresses.json`, key `cottonwood-gold-canonical-holdings`, reader ADVI_COTBKF) |
| range at its last read | 81 calendar-day partitions, 2026-06-09 to 2026-09-25 (the source file's own comment; not re-read here) | read below |
| read here | no | yes |

Whether FWD-3's gold should read the canonical store instead of the silver one is a source-declaration question (PRD v0.19 ruling 1:
a channel is an entry in `sources.json`), and it is not decided by this read.

## 3. The canonical holdings store, read 2026-10-11 ~10:3xZ

`list-objects-v2`, auto-paginated, counted client-side.

- **Objects:** 134 under the prefix; 134 are dated parquet files; 0 other.
- **Date range:** 2026-04-22 to 2026-10-09. (The record cited in msg 4704 said 2026-06-08 to 2026-10-06; the store read wider on
  both ends.)
- **Coverage:** 123 weekdays fall in the range; 120 have an object. The three without are 2026-06-19, 2026-07-03 and 2026-09-07,
  which are market holidays. 14 weekend dates also carry an object.
- **Latest object:** `2026-10-09.parquet`, last modified 2026-10-10T11:51:58Z. By the trading calendar that is the last trading day
  before today (Sunday): the store is current.

**Latest date, 2026-10-09:** 21,299 position rows, 999 accounts, 14 columns, one `source` value (`bd_snapshot`) on every row.

| a position row carries | rows | share of 21,299 |
|---|---|---|
| a market value that is not null | 14,940 | 70.1% |
| a market value that is not null and not zero | 13,571 | 63.7% |
| a market value of exactly zero | 1,369 | 6.4% |
| NO market value (null) | 6,359 | 29.9% |
| a price that is not null | 13,580 | 63.8% |

- **Accounts with at least one valued position:** 852 of 999; 147 accounts carry none on that date.
- `schwab_units` is null on every row; `holding_supervised` is true on 0 rows; `cash_equivalent` is true on 1,531.

## What this does NOT establish

- **Why 29.9% of rows carry no value.** Not read: whether they are closed or zero-unit positions carried as rows, a class the vendor
  does not price, or a defect. `units` is null on the same count (6,359), which points at rows with no position rather than unpriced
  positions; that is an inference from one equal count, not a read of the rows.
- **Whether the canonical store carries S252's lagged minority.** S252 was measured on the silver partitions, not here.
- **Any date but the latest.** One file was opened. The share on other dates is not known.
- Which securities or accounts: counts only, by instruction.
