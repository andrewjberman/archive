# L8 drain end -- ADVI_COTBKF round 10

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-07 ~12:3xZ | **For:** `3.0.0_SA_CVO` (L8 compile)

Round 10 was cut as one issuance (@770175bc0e, `fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s correction @283b15713f (msg 485):
E1 re-cut to marketdata only after this seat flagged that msg 456's 49F/INF census was cross-firm.
1 of 1 orders terminal and merged; proof VALID; 0 unmerged worker branches; 0 linked worktrees for this project.

| order | worker | drain | criteria | real run on dell2 (shared tree, after the drain) |
|---|---|---|---|---|
| CB-j-1 marketdata price output | ~26 | @7757a9529a | VALID: AC1 9 passed (BARRED-vs-USABLE control), AC2 PASS | `MARKETDATA-PRICES writer=historical-prices-scheduler bucket=opal-data-bd prefix=silver/historical_prices.parquet grade=BARRED barred_read=0 securities=0 security_days=0 gain_securities=0 gain_security_days=0 need=9388961` |

**Located, not presumed:** the registry's `historical-prices-yfinance` Lambda does not exist live (ResourceNotFound; only
`historical-prices-scheduler` across four regions). The scheduler (`infra/aws/lambda/historical-prices-scheduler/lambda_function.py:58`)
launches an EC2 that runs `data/black_diamond/scripts/silver/fetch_historical_prices_yfinance.py`, which writes
`silver/historical_prices.parquet` (`:47`, uploads `:431`, `:549`, `:783`) to its default bucket (`:43`). That bucket, `opal-data-bd`, is a
`bucket`-plane alias of the `49financial` FIRM scope in `infra/logic/registry/scopes.json`: BARRED, never read (0 S3 calls).

**FWD-3 after rounds 4-10:** every USABLE store Opal holds is now censused or measured absent -- the six legacy stores (S17), both Cottonwood
prefixes (S19, S20), and marketdata's output, which is a firm's (this round). The gap stands: **2,914 of 4,634 securities, 8,091,310 of
9,388,961 security-days** (census basis; the held basis is 3,421,735, PRD ADDENDUM 2). The residual is a vendor act under PRD v0.4
ADDENDUM 2 (Yahoo for equity/ETF/fund, Bloomberg at site Z for fixed income and other), which needs Andrew's per-use word; it is the
CTO's to put to him with these counts. Not cut.

## Rows filed in the round

| row | class | standing |
|---|---|---|
| D2-W26-S1 | OBSERVATION | INERT -- the yfinance Lambda named in the registry is not live; the writer is the scheduler's EC2 script; blind spot: the EC2's own environment could override the bucket |
| D2-W26-S2 | OBSERVATION | INERT -- marketdata's output sits in a BARRED 49financial bucket alias; whether Commonwealth may use a firm-held price table is a ruling, not a measurement |

Row ids now carry the dell2 coordinate (`-D2-`): the surprise-row gate refused the plain `W26-S<k>` form on this box. ARMED: 0.
