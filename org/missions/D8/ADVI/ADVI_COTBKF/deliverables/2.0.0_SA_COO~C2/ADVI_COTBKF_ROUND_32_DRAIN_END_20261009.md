# L8 drain end -- ADVI_COTBKF round 32

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~09:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB32af1-AC2; row
W59-S1 BLOCKING to disposition)

Round 32 was cut as one issuance @7e32953e3e (`fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2` ADDENDUM 7 @2a140ad0bb (msg
3005).

| order | item | worker | state |
|---|---|---|---|
| CB-af-1 | read-only trace of the chain's base close for SCHB / SCHZ | ~59 | complete @89b2c09855, drained @f1c4cda7f0 |

## The real run, shared tree, after the drain

```
BASE-TRACE cusips=2 adj_close_base=0 stale_carry=0 other_source=2 untraced=0
```

The issuer's run matches the worker's.

## What the round found

**The source** is the same for both CUSIPs:
- the store `cottonwood-silver-canonical-prices` at `s3://opal-data-cot/silver/prices/canonical_prices.parquet`;
- series key `ticker`, field `price`, row date 2022-10-12 (same-day, no carry-forward);
- the row's own source label is `yahoo_finance`.

| CUSIP | chain price | Yahoo Close | Yahoo Adj Close | chain / Close (range) | chain / Adj Close |
|---|---|---|---|---|---|
| 808524102 SCHB | 13.3302 | 13.98 | 13.259 | 0.9214-1.0000 (15 days) | 1.0054 on every sampled day |
| 808524839 SCHZ | 19.7181 | 22.465 | 19.3014 | 0.8777-1.0000 (8 days) | 1.0216 on every sampled day |

- **By the pre-written rule: `other_source` for both.** A constant ratio to today's Adj Close, off by more than the 0.5% test, does not
  meet `adj_close_base`.
- **Reading (worker and issuer, INFERRED):** the store holds a DIVIDEND-ADJUSTED Yahoo series from an earlier fetch vintage. Each new
  dividend rescales Yahoo's adjusted history by a constant, which is exactly the shape of a constant 1.0054 / 1.0216.
- Sampling caveat: first-of-quarter calendar days are often `linear_interpolation` rows in the store with no Yahoo bar. They were
  skipped by the rule and are listed in the md.

## Why this is a methodology question, not a two-CUSIP repair (issuer, INFERRED -- for the CTO's ruling)

- The store is the chain's price source for every security it values, not only these two. If its `price` is dividend-adjusted
  throughout, every pre-dividend day of every dividend-paying holding is valued below as-traded.
- The chain also books dividends as cash (`dv` / `dvr` through the cash ledger, CB-ab-1's rule 2). With an adjusted close, the
  price does not drop on the ex-date while the cash rises. The dividend can then count twice in a daily return, by about the
  distribution's size on each ex/pay day.
- That would bear on month grades near distributions, on the round-28 `DVR_CLOSE_STEP` signature, and on the W53-S3 dividend
  regressions. It is unmeasured.
- Round 28's `method_r28` split rule says "the stores' closes are split-adjusted over their whole history". The trace shows they
  are also dividend-adjusted.

**Rows:** W59-S1 (BLOCKING, INERT). ARMED: 0.

**Round-close check:** REFUSED on the one ungraded judgment criterion, CB32af1-AC2. Orders 1/1 complete.
