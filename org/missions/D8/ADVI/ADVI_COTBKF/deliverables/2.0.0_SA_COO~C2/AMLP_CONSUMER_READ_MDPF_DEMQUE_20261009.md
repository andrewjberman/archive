# AMLP consumer read -- ADVI_COTBKF reading dell1 MDPF_DEMQUE's Yahoo price store (2026-10-09 ~01:4xZ)

**Asked by:** dell1 `2.0.0_SA_COO~Q1` (msg 1352, relayed as dell2 msg 2089): "value one living client's AMLP holding on its
backfilled dates from this store and report agreement with trade prices -- that read closes FWD-1." **Read by:** `2.0.0_SA_COO~C2`.
Read-only; no write anywhere.

**Inputs** (addresses from `lib/opal_naming.address`, except the store's, copied from the contract @8abd95ad3b, which says it copied
`address()`):
- transactions: `s3://opal-data-assets/commonwealth/cottonwood/silver/transactions/date=2026-06-23`
- crosswalk: `s3://opal-data-assets/commonwealth/cottonwood/silver/crosswalk/date=2026-06-23/crosswalk.parquet`
- store: `s3://opal-data-assets/yahoo/global/silver/price_history/cusip=00162Q866/prices.parquet`, valued with `as_traded_close` per the
  contract. 3,323 rows, 2013-04-08..2026-06-23.

## Result

- **Population:** 890 AMLP transaction rows on 99 accounts; 471 accounts are MATCHED (living clients) in the crosswalk.
- **Account chosen:** acct#8039e07b, MATCHED, the living client with the most AMLP rows (43).
- **Valuation:** quantities signed by the chain's own table (`commonwealth_signs`: plus `by` `dvr` `li`, minus `sl` `loca`, `dv` no
  quantity). The account held AMLP from **2016-03-04 to 2020-05-15**, giving **1,058 valued days**, every one priced from the store (0 unpriced).
  - Peak quantity 15,724.494; peak value 97,162.55 on 2017-05-23.
  - Last held day 2020-05-15: 15,724.494 x 4.8100 = 75,634.81.
  - The `loca` transfer out takes the quantity to 0.000000. This matches the 2026-06-23 position snapshot, which has no AMLP row for
    the account.
- **Agreement with trade prices** (|trade price / store close - 1| <= 2%): **3 of 4** buys and sells agree. The median error is 0.92%.

  | date | type | qty | trade price | store as-traded close | error |
  |---|---|---|---|---|---|
  | 2017-05-18 | by | 1,000 | 12.3070 | 12.12 | 1.54% |
  | 2019-07-03 | sl | 2,000 | 9.9998 | 9.98 | 0.20% |
  | 2020-02-03 | by | 2,500 | 7.9833 | 7.96 | 0.29% |
  | 2020-03-12 | by | 5,000 | 4.0010 | 3.84 | **4.19%** |

  The one miss is 2020-03-12, the COVID-crash day, when an intraday fill can sit far from the close. It is a reading, not a defect.

## Correction made during the read

My first pass counted only `by`/`sl` quantities and valued a phantom 6,500 shares through 2026-06-23. It ignored the `li` transfers in,
the `dvr` reinvestments and the `loca` transfer out. The figures above use the chain's full sign table. The phantom figure was never sent.
