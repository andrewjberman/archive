# IRPT_YCDGEN round 10, cells YCD-b-10 and YCD-c-10 -- what the store's source describes by kind, and the one account three ways

**By:** `2.0.0_SA_COO~G2`, 2026-10-11, read-only, NO pull, on the CTO's round-10 analysis @ea78b95649 section 4 items 2 and 3.
Counts and percentages only; no account id, symbol or dollar figure. Record: `STORE_BY_KIND_AND_THE_ONE_ACCOUNT_20261011.json`.

## 1. YCD-b-10: on the store's existing 172 rows, which kinds carry a country and a sector

Store `s3://opal-data-etfs/bbg/2026-10-09/characteristics.parquet`. Kind is read two ways: the asset type the transactions
cache gives the row's symbol, and the store's own fund columns (`FUND_EXPENSE_RATIO`, `FUND_TOTAL_ASSETS`).

| kind (transactions cache) | rows | with a country | with a sector | with a fund column |
|---|---|---|---|---|
| Equity | 127 | 127 | 127 | 0 |
| not in the transactions cache | 43 | 43 | 37 | 6 |
| ETF | 2 | 2 | 0 | 2 |

| by the store's own fund columns | rows | with a country | with a sector |
|---|---|---|---|
| rows that carry a fund column | 8 | 8 | **0** |
| rows that carry none | 164 | 164 | 164 |

**Reading.** Every one of the 8 fund rows carries a country and NONE carries a sector; every one of the 164 other rows
carries both. So on today's evidence the source gives a fund a country of DOMICILE and no sector. Three things follow:
- a pull of fund symbols buys NO sector section;
- it buys a country, but a fund's domicile is not the regional exposure of what the fund holds, so a `region_exposure_*`
  section fed from it would state the fund's home country for the whole position. Whether that is a true figure for the
  page is a judgment for the reviewer and the CTO, not a count;
- the store holds NO mutual fund and NO cash symbol at all (0 rows of either kind), so whether the source describes those
  kinds is NOT observed. The 2 rows the transactions cache calls ETF and 6 more rows with fund columns are the only funds.

The 14-symbol list by kind: ETF 5, Mutual Fund 4, Mutual Fund (Closed End) 2, Cash 1, Cash Equivalent 1, Equity 1.
Describable on this evidence: for a sector, the 1 equity; for a country, the 1 equity and the 5 ETFs (6 of 14).

## 2. YCD-c-10: the accounts of six or more positions, three ways

Positions of 2026-05-06. Eligible (all positions priced and symbolled) accounts with six or more positions: **8**.
Each row is one account; no id is written. 'Describable' adds only those of the 14 the store shows that input for.

| positions | kinds held | covered today (country / sector) | after all 14 | after the describable of the 14 (country / sector) |
|---|---|---|---|---|
| 10 | Equity 9, Cash 1 | 76.85% / 76.85% | 93.09% | 91.29% / 91.29% |
| 10 | Equity 6, Cash Equivalent 1, ETF 1, Mutual Fund (Closed End) 1, Cash 1 | 65.40% / 59.43% | 84.31% | 65.40% / 59.43% |
| 9 | ETF 8, Cash 1 | 0.00% / 0.00% | 83.36% | 79.73% / 0.00% |
| 10 | ETF 9, Cash 1 | 0.00% / 0.00% | 76.44% | 70.86% / 0.00% |
| 10 | ETF 9, Cash 1 | 0.00% / 0.00% | 72.93% | 70.07% / 0.00% |
| 8 | Equity 6, Cash Equivalent 1, Cash 1 | 39.06% / 39.06% | 72.28% | 39.06% / 39.06% |
| 6 | Equity 4, Cash Equivalent 1, Cash 1 | 36.49% / 36.49% | 69.72% | 36.49% / 36.49% |
| 22 | ETF 20, Equity 1, Cash 1 | 0.00% / 0.00% | 3.59% | 0.00% / 0.00% |

**The one account.** 10 positions (Equity 9, Cash 1). Covered by value: **76.85% today**, **93.09% after all 14**, and
**91.29% after only the describable of the 14**, for country and for sector alike. The describable addition that moves it
is the ONE equity symbol of the 14; its cash position is the remainder. It is the only eligible account of six or more
positions that reads 90% either way. The next reads 84.31% after all 14 and 65.40% on the describable subset.

## 3. Limits

- 8 fund rows is a small sample, and none is a mutual fund; 'the source gives funds no sector' is observed on ETFs only.
- Coverage is of PRICED value on one date, five months old; the account's holdings today are not read.
- 'Covered' means a store row exists with that input non-null. The Overview's own coverage rule for a section was not run.
- A symbol match is assumed to be the same security.
