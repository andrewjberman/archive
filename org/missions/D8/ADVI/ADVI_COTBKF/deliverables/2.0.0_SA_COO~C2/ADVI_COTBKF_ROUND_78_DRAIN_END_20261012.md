# L8 drain end -- ADVI_COTBKF round 78: the flat-charge reading FAILS its own held-out bar (real, far above chance, incomplete); the price store holds NO unadjusted close for the 15 funds (a cache on one box does, for every held trading day); the ruling on row D2-S131 is in the list

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-12 ~01:36Z | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB78bz1-AC2, CB78bz2-AC2)
**Cut on:** `1.0.0_SA_CTO~DELL2` round-78 analysis @e5d2fc8e59 (the hash read from the file's own history). **Issued:** @c187a85a58, 3 cells
(2 at once; the list after both drained).
**Nothing was built, applied, served, re-minted or fetched from a vendor. One store object of this project's firm was read (a head
and a get), read-only.**

| order | item | worker | state | issuer's own run at the drained base |
|---|---|---|---|---|
| CB-bz-1 | the causes of the trades that miss the price paid, to completion | ~148 | complete @42b9154389, drained | `PRICE-PAID-CAUSES test_written=True constants=7 held_out_units=13009 held_out_fits=12629 held_out_fits_none=380 ... in_sample_units=935 in_sample_fits=935 reading=fails still_off=727 given=727 none_found=92 change_with_the_order=161` |
| CB-bz-2 | the store's field for the unadjusted close | ~149 | complete @3e43277e68, drained | `STORE-FIELD funds=15 listed=15 store_holds_an_unadjusted_close=False with_a_store_field=0 schema_columns=5 ... held_dates_total=29834 covered_by_store_total=0 covered_by_cache_total=20718 uncovered_trading_days_total=0` |
| CB-bz-3 | the correction list brought current (direct-act; the issuer's addition) | ~150 | complete @4739edbc6e, drained | `OPEN-CORRECTIONS-RECORD revisions=8 record_absent=0 in_force=True causes=True store_field=True state=OPEN corrections=6 keys_complete=True evidence_rows=46 unreconciled=45` |

No product code changed (records and three channel rows), so the suite was not re-run: it stands at `1020 passed, 12 skipped`.
The issuer ran each record's line at the base, read the writer's and the landing's cited lines itself (section 2), and re-derived
no count this round; the counts are the workers'.

## 1. For L9: CB78bz1-AC2 (the causes, to completion)

**The test, stamped 01:06:59Z, before any row of this round was looked at.** The hypothesis with round 76's seven dollar figures
fixed (0, 3, 10, 15, 19, 30, 34; a 15-cent window; a purchase's amount above shares times the unadjusted close, a sale's below);
two held-out populations that were not used to read the figures; a chance control (the figures shifted together four ways); and
the bar: it HOLDS only if, on each held-out population separately, at least 90 percent of units fit the seven AND at least 90
percent of the units with a nonzero gap fit a nonzero figure, with the best shifted set at or under 20 percent.

**The result: `fails`.**

| held-out population | informative units | fit the seven | units with a nonzero gap | of them, fit a nonzero figure | best shifted set |
|---|---|---|---|---|---|
| the substituted funds | 10,541 | 98.2 percent | 643 | 71.1 percent | 0.47 percent |
| seven failing funds outside round 76's nineteen | 2,468 | 92.1 percent | 341 | 43.1 percent | 0.29 percent |

The figures are far above chance and they are INCOMPLETE: 380 held-out units fit none. In sample, 935 of 935 fit and round 76's
counts reproduce exactly, which is an implementation check and not evidence. The sales of the nineteen, which round 76 had seen,
are reported apart (98.8 and 98.6 percent).

**For the grade:**
- **Most of the "fit the seven" share is the zero figure:** 12,025 of 13,009 held-out units have no gap at all. The second column,
  on units that DO have a gap, is the one that tests the charge, and the worker wrote that column into the bar before the run.
- **Post hoc, the worker's, in no count:** a gap near 12 dollars on most units that fit none (101 of 186, 171 of 194, 10 of 11).
  Read off those same units: a description, not a test.
- **The charge, from the rows:** it goes with the fund family, the kind of row and the trade size, and not with the account-day
  (of 4,848 account-days with two or more units, 1,611 carry one nonzero figure beside a zero-gap unit). Nothing on disk names it:
  no fee column; a fee-type row sits on the same account-day for 0.59 percent of charged units against 0.54 percent of uncharged.
  What the charge is, is not established.
- **Still off, 727 units, all given a cause:** under the stated order the flat charge 431, a neighbouring day's close 165, a
  reinvestment or exchange 33, an adjusted close 6, none found 92; under the alternative the flat charge 592 and none found 92.
  **161 change with the order.** Round 76's 124 none-found rows all take a cause now; 92 other units do not.
- **VEIRX:** a flat gap on 1,584 of its 1,596 units; a unit is off exactly when the gap exceeds 1 percent of the amount (343 of 343
  above, 0 of 1,253 below).
- **Because the reading fails, the shares are plain:** the unadjusted close reproduces the price paid on 73.7 percent of purchases
  of the nineteen funds, 87.1 percent for the 15 failing funds, 98.1 percent for the substituted; sales 89.2, 89.6, 97.7.
- **Row D2-W148-S1, an error caught by the worker's own check:** it first built on the served close for the nineteen funds, which
  is not their unadjusted close; its in-sample fit came out at 2 of 936; it switched to the unadjusted close the test text defines.
  No constant, window, threshold or order changed. The issuer's prompt listed both closes under one heading.

## 2. For L9: CB78bz2-AC2 (the store's field)

**The store holds no unadjusted close.** Its schema, read from one get of the store object (last modified 2026-10-09T13:41:04Z;
11,289,398 rows): `date`, `asset_name`, `ticker`, `price`, `source`. ONE price column. For all 15 funds that price equals the
cache's unadjusted close on 3.2 to 10.2 percent of dates, and is not the cache's adjusted close times one constant either.
The writer carries one price by design: it takes the `close` column of the historical-prices landing
(`build_canonical_prices_v2.py:822`), and the landing upstream declares one price column
(`land_cot.py:23`; `close` = `as_traded_close` at `:150`). The issuer read those three lines itself.

**The dates the back-fill reads.** 29,834 held dates over the 15 funds: 0 covered by a store field; 20,718 covered by the vendor
cache, which is every held trading day (the earliest held day is 2020-07-06; the other 9,116 are non-trading days the build
interpolates); 0 held trading days uncovered. **The fifteenth, VGHAX, lacks trades to test on, not a field or dates:** 5 trade
units, 1 within 1 percent; the cache covers all 1,441 of its held trading days.

**For the grade:**
- "The cache is a file on one box and not a store a build reads" (the record's words). A corrected basis has no store to come from.
- That the store's price is a dividend-adjusted series as of an earlier pull is INFERRED from the two comparisons; no field says so.
- **Row D2-W149-S1:** the live store object is not the output of the writer at HEAD (it has no `source_firm` column, which the
  writer writes; it carries a `scoped_override` source on 12,042 rows, which the writer never assigns).
- **Row D2-W149-S2:** the store's ticker key is not one security: 308 of 4,000 tickers carry more than one asset name; 5,748,151 of
  11,289,398 rows have no ticker; VGHAX carries three names. The build reads the store by ticker.
- The worker loaded the whole object (this firm's) to read it; beyond the 15 tickers it printed two aggregate counts and no price.
- Not established: what `close` means at the vendor in the landing; who loaded these funds' rows; the price basis of the 680
  fund-days after 2026-06-09 that come from the holdings snapshot.

## 3. The correction list (`deliverables/OPEN_CORRECTIONS.json`, revision 8, six entries)

- **The ruling in force is in it,** under `in_force` on the merged entry, quoted with its lines: no rebuild of a holdings partition
  dated before 2026-06-08 for this firm; no consumer attached to the minted table; by any lane; until the fund basis is fixed and
  proven. A pointer at the top level, `rulings_in_force`. `state` stays `OPEN`.
- This round's two records are in the merged entry's extent. The round-76 item about 124 none-found rows is replaced by what the
  test shows, and stays open. Five new unreconciled items, among them: round 77 found the unadjusted close in a cache, round 78
  finds the store holds none; and the 15 failing funds were classed with a 34.15-dollar allowance whose seven figures have now
  failed their bar as a complete set, and are not re-classed here.
- The worker's own check: the first 43 evidence rows unchanged and in order; of the former unreconciled strings only the one
  replaced differs. 45 unreconciled items in all. No PRD addendum past v0.7 exists.
- **This cell is the issuer's addition:** the analysis lists no list item. Said in the decomposition, for the CTO.

## Where this leaves the project

- **The two inputs the fund-basis addendum waits on, as they came out:** (1) the trades that miss the unadjusted close are mostly a
  flat dollar gap whose figures are real and incomplete; the test failed its bar, so the rule still has 26 percent of the nineteen
  funds' purchases against it by the plain count; (2) the store holds no unadjusted close: the only one is a cache on one box,
  which does cover every held trading day.
- **In force:** no rebuild of the early holdings partitions; no consumer on the minted table.
- **Not decided here, the CTO's:** what the addendum names as the basis and where a build is to read it from; whether the flat gap
  is set aside by a rule (and with which figures) or the test is re-run with a figure added; who owns the price store and its
  ticker key; the carried portal page binding; the addendum for the 2022 factor; when the list closes.
- No re-mint order is cut. The served table is `method_r28`'s. The tree's default is `method_r29`.

**Round-close check:** REFUSED until the two judgment criteria are graded.
