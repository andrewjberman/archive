# L8 drain end -- ADVI_COTBKF round 33

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~11:1xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB33ag1-AC2)

Round 33 was cut as one issuance @0a2c4cb744 (`fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2` ADDENDUM 8 @bff4e48547 (msg
3060), the as-traded ruling. Items 2 and 3 (marking and rebuild under a pair; SCHB re-read) depend on this census. They are drafted
@a9a774a7b9 and cut on the analysis.

| order | item | worker | state |
|---|---|---|---|
| CB-ag-1 | per-ticker price-basis census of the chain's store; served account-days on adjusted prices; `bd_txn_price` provenance | ~60 | complete @3a063e09a6 (rule commit e5b8ad94ba first), drained @aa376eb868 |

## The real run, shared tree, after the drain

```
yahoo cache: 3580 of 3580 tickers reused, 0 to fetch
PRICE-BASIS tickers=3580 as_traded=175 dividend_adjusted=2079 indistinguishable=872 mixed=79 no_yahoo=109 other=266 yahoo_calls=0 adv_days_on_adjusted=638948/1669040
```

The issuer's run matches the worker's on every count. It ran from the worker's cache (copied before the worktree was removed), so it
made 0 Yahoo calls. The worker's one pass made 72 (73 with its debug call, row W60-S2), paced at 50 tickers per call, 6 s apart, with
no rate-limit.

## What the round found

**The store** `s3://opal-data-cot/silver/prices/canonical_prices.parquet` (LastModified 2026-06-09 20:42:16Z): 11,291,021 rows, 4,003
tickers. Of the 3,580 tickers with `yahoo_finance` rows:

| class | tickers | share |
|---|---|---|
| dividend_adjusted | 2,079 | 58.1% |
| indistinguishable (no dividends in window) | 872 | 24.4% |
| other (239 match neither basis) | 266 | 7.4% |
| as_traded | 175 | 4.9% |
| no_yahoo | 109 | 3.0% |
| mixed | 79 | 2.2% |

- The implied vintages of the adjusted tickers cluster at dividends through ~2026-03 (985 tickers) and ~2026-02 (363).
- Store rows resting on adjusted or mixed tickers: 3,301,733 of 11,227,207 (29.4%). That is 2,257,024 Yahoo rows plus 1,044,709
  interpolated rows.

**The served FWD-3 tables rest materially on the wrong basis.** In `account_day_value` (21,102,041 rows), at least one holding is priced
from an adjusted or mixed ticker on:
- 638,948 of 1,669,040 account-days (38.3%);
- 688 of 1,528 accounts;
- 31,249 of 81,718 account-months, in 73 of 159 months (2020-06 on).

That is ADDENDUM 8 item 2's condition: the rebuild under a pair is owed, and the affected rows are marked until it lands. The
CUSIP-to-ticker map is the current silver transactions, an approximation of the run-date map that the worker disclosed.

**The rebuild needs no second Yahoo pass.** The cached pulls hold `Close` (split-adjusted, dividend-unadjusted) for all 3,580
tickers. The draft @a9a774a7b9 covers it: CB-ag-2 `method_r33` + re-grade; CB-ag-3 marking + rebuild on `0.7.0_AE_CloudOps~CB2`.

**`bd_txn_price` (row D2-S48 -> W60-S1), for the CTO, possibly law-class (cross-firm):**
- Three bond CUSIPs in the cottonwood store carry it: 05613L3H2, 651639AX4 and 95000U2D4, 1,623 rows from 2024-01 to 2026-06, at
  prices ~0.90-1.02 of par.
- The only writer in the repo is `data/black_diamond/scripts/silver/inject_scoped_overrides.py:136`, with values from
  `data/black_diamond/scripts/silver/scoped_price_exceptions.json`. There is no cottonwood writer.
- How the rows reached the `opal-data-cot` store is unread; reading the bd side is barred.
- If `black_diamond` here is the bd firm's pipeline, a cot pipeline tree is reading another firm's data (CLAUDE.md NEVER, "cot is a
  separate firm from bd"). If it is a shared Black Diamond platform step that wrote cottonwood-scoped exceptions, it is not.
- The issuer does not rule this. It goes to `1.0.0_SA_CTO~DELL2` with the slug.

**Rows:** W60-S1 (bd_txn_price provenance, INERT) and W60-S2 (the 73rd Yahoo call, INERT). ARMED: 0. Row D2-S48 is folded into W60-S1.

**Round-close check:** REFUSED on the one ungraded judgment criterion, CB33ag1-AC2 (rule commit e5b8ad94ba precedes output 3a063e09a6;
the worker reports the script unchanged between them).
