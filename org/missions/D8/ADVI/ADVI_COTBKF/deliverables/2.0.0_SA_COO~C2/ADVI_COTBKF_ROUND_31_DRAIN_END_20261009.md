# L8 drain end -- ADVI_COTBKF round 31

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~09:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile; no judgment criterion; row
W58-S1 BLOCKING to disposition)

Round 31 was cut as one issuance @97707c3b8d (`fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2` ADDENDUM 6 @d6e3227fd7 (msg
2968).

| order | item | worker | state |
|---|---|---|---|
| CB-ae-1 | Yahoo as-traded close of 808524102 / 808524839 on 2022-10-12, stored as evidence, branch by a pre-written rule | ~58 | complete @c09f3ffd56, drained @f5689476e2 |

## The real run, shared tree, after the drain

```
LEVEL-PROBE cusips=2 branch=OTHER key=s3://opal-data-assets/commonwealth/cottonwood/silver/price_evidence/date=2022-10-12/part-00000.parquet readback_rows=2
STORED EVIDENCE MATCHES fresh fetch (same evidence; read back, not rewritten)
```

The issuer's run matches the worker's. The one S3 write is a new evidence key (head-object read it absent first), read back 2 rows.

## What the round found

| CUSIP | symbol (source: delivery Symbol column) | Yahoo Close (split-adj.) | Yahoo splits after | as-traded | r28 | r26 |
|---|---|---|---|---|---|---|
| 808524102 | SCHB | 13.98 | 2024-10-11 x3 | 41.94 | 39.9906 | 13.3302 |
| 808524839 | SCHZ | 22.465 | 2024-10-11 x2 | 44.93 | 39.4362 | 19.7181 |

- Yahoo's split series names the same ratios on the same day as the account rows (x3, x2).
- **By the pre-written rule: branch OTHER.** Neither CUSIP is within 2% of either level. Row W58-S1 is BLOCKING, so neither branch is
  assumed.
- **Issuer arithmetic on the printed values** (MEASURED from the table, the reading INFERRED):
  - as-traded / r26 = 3.146 and 2.279. That is the split factor (3, 2) times a residual.
  - r26 close / Yahoo adjusted Close = 0.954 and 0.878. The same residual is already in r26's base close, before any split scaling.
  - So the split scaling r28 applies agrees with Yahoo's split series. The gap that remains (-4.9% / -12.2%) sits in the chain's
    BASE close for these two CUSIPs on this day, under BOTH methods.
- SCHZ is on the ranked need list as unpriced through 2022-10-11. Where the chain's 19.7181 comes from is unmeasured.

## Proposed for the analysis (not decided here)

- **(a)** Treat the split question as answered: r28's factor matches Yahoo's split series and the outside level is ~3x / ~2x r26. On
  that reading D2-S45's "which level" goes to r28. The residual becomes a separate base-close finding.
- **(b)** A read-only trace of where the chain's 2022-10-12 close for SCHB and SCHZ comes from (source, date, carry-forward) against
  Yahoo's series over the held window.

**Rows:** W58-S1 (BLOCKING, hazard INERT; owner disposition at L9/L10). ARMED: 0.

**Round-close check:** MAY-CLOSE (orders 1/1, judgment 0). The BLOCKING row needs its disposition before the slug.
