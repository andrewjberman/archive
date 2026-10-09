# ADVI_COTBKF -- ROUND 33 dependent cells, DRAFT (issuer prep, NOT an issuance) -- 2.0.0_SA_COO~C2, 2026-10-09 ~10:1xZ

This draft was written while `CB-ag-1` (the price-basis census, worker ~60) runs. These cells are cut on its result, under ADDENDUM 8.
They carry no authority before then.

## CB-ag-2 -- the as-traded price input and the chain change (LOCAL)

- **Input.** For every ticker the census classes `dividend_adjusted` or `mixed`, take Yahoo `Close` (split-adjusted, never
  dividend-adjusted) from the census's raw cache `.scratch/advi_cotbkf/yahoo_census/`. This needs no second Yahoo pass.
- **The rule, `method_r33`, committed alone before the run.** The valuation reads that as-traded series in place of the store's
  `yahoo_finance` rows for those tickers. Interpolated days are re-derived between the as-traded points by the store's own
  interpolation rule. The rows are not rescaled.
  - r28's split scaling still applies on top. The `Close` series is split-adjusted, so as-traded = `Close` x the splits after the day.
  - Dividends stay cash-only.
- **Re-grade.** Run `method_r28` -> `method_r33` with the sweep runner. Print MATCH/DIFF/UNGRADABLE, regressions and movers back. The
  4 ABSENT months (W53-S3) are re-read; the expectation is that the dividend double-count was their cause, which is unmeasured until
  this run. SCHB's 2022-10-12 level is printed beside the round-31 evidence key.
- **Open, to be decided by the census:** tickers classed `no_yahoo` keep the store price, labelled `price_basis: store_unverified`.

## CB-ag-3 -- marking, then the rebuild, SERVED, on `0.7.0_AE_CloudOps~CB2` under a never-widen pair

- **Step 1, the marking.** Add a `price_basis` column to the three served tables: `dividend_adjusted (known wrong; rebuild owed)` on
  the rows the census counts, `as_traded` elsewhere.
  - This rewrites the three keys whole, so it is a served move under a pair.
  - Because 0 readers exist and the rebuild follows directly, the pair may name the marking and the rebuild as ONE act with ONE
    rollback (the @476f970245 versions). That is the CTO's call at the CTO half.
- **Step 2, the rebuild.** Rebuild at `method_r33`, read back with `--verify`, and close the ledger.
  - The order carries the deploy_ledger interim rule (MSTR msgs 2908 / 2974 / 3033): commit after `open` and after each leg, unless
    fix @00d3393ff3 is in dell2 HEAD at cut time.
- **Pair halves.** The COO half names every table, its key, its row count before and after, and the rollback version per key. Both
  branches are covered: the 4 months come back MATCH, or stay ABSENT.
