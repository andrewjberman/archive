# READ 3 -- does the scanner's own source carry a currency

Read for `2.0.0_SA_COO~Z`, AMGT_RESAPP round 78, 2026-10-07. Ruling:
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULINGS_AMGT_RESAPP_ROUND78_CALLS_AT_THE_CUT_20261007.md`, bb-8: "one
read of whether the scanner's own source carries a currency. If it does, the scanner's producer serves it. If it does
not, it is one added Bloomberg reference field and is Andrew's word." Workspace HEAD at the read `3366536af5`. Script:
`round78/checks/r78_read_scanner_currency.py`; its literal output `round78/reads/scanner_currency_read_output.txt`
(all 339 column names are printed there); every figure `round78/reads/SCANNER_CURRENCY_READ.json`.

## The answer in three lines

1. **No. The upstream source carries no currency, per row or per listing.** It is one FactSet screening workbook of
   2,869 rows and 339 columns; 0 columns name a currency, 0 text columns hold currency codes, and its report header
   says nothing about one.
2. **Rows that would gain a currency if the producer passed it through: 0 of 651.** There is nothing to pass.
3. **What the workbook does carry and the producer drops:** each row's SEDOL, ISIN and CUSIP, and the exchange's
   country code. Those identify the listing; they are not a currency, and the ruling bars inferring one from an
   exchange code. So bb-8's remainder is the added Bloomberg field, which is Andrew's word.

## The chain

| hop | object | read |
|---|---|---|
| the peer rows | served `peers.members` on `GET /security/<name>/overlay` | deployed function, 95 covered names |
| the scanner files | `s3://opal-data-portal-v2/json/security_scanner/latest/universes/<id>/universe_data.json`, six universes; reader `lib/research/peers/universe.py:417` | S3 GET of all six |
| the producer | `infra/aws/lambda/opal_security_scanner_processor/lambda_function.py`, `lambda_handler` (`:299`), rows built by `_build_universe_rows` (`:208-248`) | the code |
| **the upstream source** | `s3://opal-data-portal-v2/security_scanner/uploads/2026-10-02/Screening_DIVZ_IDVZ_20261002.xlsx`, read by the producer as `pd.read_excel(buf, header=4)` (`:325`) | S3 GET, opened the same way |

The workbook read is the one the served files were built from: its folder `2026-10-02` equals the six files' `asOf`,
and it was stored at 2026-10-02T16:37Z, one minute before the six files (16:38Z).

## The scanner files (the producer's output)

| universe | rows | with a price |
|---|---|---|
| acwx | 1,833 | 1,830 |
| eafe | 645 | 644 |
| eafev | 390 | 389 |
| r1000 | 1,023 | 1,022 |
| r1000v | 870 | 869 |
| sp500 | 503 | 502 |
| sum | 5,264 | 5,256 |

- Row fields over the six files: 10 (`ticker, name, mktVal, country, sector, industryGroup, universeWeight,
  divzWeight, price, values`). Fields naming a currency: 0 of 10. Factor codes naming a currency: 0 of 284. Top-level
  keys naming one: 0. This repeats GROUP_B_NOTES cell B2 on today's files.
- Three more folders sit under the same prefix (`msciusa`, `rmidcap`, `sp400`, each stored 2026-05-20). The producer
  does not write them today (its `UNIVERSE_MAP`, `:46-53`, names six) and they carry no `price` field. Not read
  further.

## The upstream source (the producer's input)

| | |
|---|---|
| object | `security_scanner/uploads/2026-10-02/Screening_DIVZ_IDVZ_20261002.xlsx`, 9,170,384 bytes |
| sheets | 1 (`Tab1`) |
| report header (rows 1 to 4) | row 1 "FactSet Universal Screening"; rows 2 to 4 empty |
| data rows | 2,869 |
| columns | 339 |
| **columns whose name names a currency** (currency, ccy, crncy, fx, iso, denom) | **0 of 339** |
| **text columns whose values are currency codes** (three capitals, the set including USD) | **0** |
| the report header mentions a currency | no |

Four column names begin "curr" and are not currencies: `curr_ratio`, `curr_ratio_chg_1yr`, `curr_asset_liq`,
`curr_asset_liq_chg_1yr`. They are the current ratio and current-asset liquidity factors; every value is a number
(for example 2.45763).

The fields of the upstream source, by group (all 339 names are in the output file):

| group | columns | passed to the scanner row |
|---|---|---|
| identity | `ticker, name, date_biz, permid, cusip, sedol, isin, is_primary, parent_equity` | `ticker`, `name` only |
| labels | `country_name, sector_name, indgrp_name` | all three (`country`, `sector`, `industryGroup`) |
| universe and model weights | `wt_ivv, wt_iwb, wt_iwd, wt_acwx, wt_efa, wt_efv, wt_divz, wt_idvz, wt_pfde, wt_pfoe` | the universe's own weight and `wt_divz` |
| listing | `adr_flag, primary_list, price, price_split, price_unadj, shares, shares_est, return, return_price` | `price` only |
| dates | `days_since_rpt, days_to_rpt, date_rpt, date_fiscal, date_rpt_fq, date_fiscal_fq, num_emp` | none |
| countries | `country_hq, country_exch, country_incorp, country_rev, country_risk, country_conc` | none |
| classification codes | `economy, sector, subsec, indgrp, industry, subind` and four `_conc` columns | none |
| size | `mkt_val, mkt_val_sec, midcap, ev, bv, sales, assets` | `mkt_val` as `mktVal`; the rest as factor values |
| factors | the remaining columns | as `values` (284 codes) |

What the workbook holds about each listing:

| column | non-null of 2,869 | distinct | examples |
|---|---|---|---|
| `price` | 2,866 | 2,701 | 2510.0, 276000.0, 1833000.0, 14.37 |
| `country_exch` | 2,868 | 47 | TW, KR, NL, HK, GB, CA |
| `country_name` | 2,868 | 47 | TAIWAN, SOUTH KOREA, NETHERLANDS |
| `adr_flag` | 2,866 | 2 | 0, 1 |
| `primary_list` | 2,866 | 2 | 1, 0 |
| `isin` | 2,868 | 2,867 | TW0002330008, KR7005930003 |
| `sedol` | 2,868 | 2,867 | 6889106, 6771720 |
| `cusip` | 2,868 | 2,867 | Y84629107, Y74718100 |
| `mkt_val` | 2,866 | 2,784 | 2040450.0, 1308790.0 |

The prices are plainly not in one currency (276,000 and 1,833,000 beside 14.37), and no column says which. The
producer names `price`, `isin`, `sedol`, `cusip` and `country_exch` in its list of columns that are not factors
(`NON_SCORING_COLS`, `:60-84`); that list holds no currency column either.

## The served peer rows

Deployed `/overlay`, 95 covered names, 95 of 95 answered 200.

| | rows |
|---|---|
| names with a peer set | 57 of 95 |
| peer rows | 676 |
| with a price | 676 of 676 |
| of those, with a price currency | 25 |
| of those, without | 651 (United States rows 491, other countries 160) |
| **would gain a currency from a producer pass-through** | **0 of 651** |

The 651 and the 25 equal GROUP_B_NOTES cell B2. The ruling's "about 600" is that cell's estimate of what stays
unreachable after bb-8's own build (651 less about 50).

## One further count: the identifiers the producer drops

Measured because the workbook carries it. It is not a currency source.

- All 651 rows are in the workbook by ticker, and all 651 have a SEDOL or an ISIN there.
- The pool list (`crosswalk/v1/2026-10-07.json`) stores a SEDOL and an ISIN for 65 of its 243 records.
- Rows whose workbook SEDOL or ISIN equals a pool record's: **50 of 651**, over 24 distinct tickers (`028758`,
  `712387`, `B288C9`, `BMVRB7`, `BRJL17`, and 19 US tickers from ABNB to ZTS).

So if the producer passed SEDOL and ISIN through, a peer row could be matched to a pool record by its exact listing
and not by company name: the match that would have refused Taiwan Semiconductor's Taiwan price against the US
listing's record. It reaches the same order of rows bb-8 already reaches by US ticker (about 50), and it gives a
currency only where the matched record states one. It does not close the 600.

## NOT MEASURED

- **Whether FactSet can add a currency column to this screen.** The workbook is a saved FactSet screen; what other
  fields the screen could export was not asked of anyone and is not in any stored object read here.
- **The older uploads** (`2026-02-26`, `2026-05-18`, `2026-08-06`, `20260519`, `20260521`) were listed, not opened.
  The answer is for the workbook the served files were built from.
- **The currency each price is actually quoted in.** Nothing stored says. The magnitudes suggest each listing's own
  currency; that is an inference and is not used.
- **Whether the 50 matched records each state a trading currency.** The match was counted; the records' currency
  field was not opened (the same gap GROUP_B_NOTES B2 item 4 states).
- **The producer was read as code and not run.** Its deployed bytes were not compared with the file in the repo.
- **The other scanner artefact**, `scanner_data.json` (built by `_build_scanner_rows`, `:251-292`), has the same row
  fields plus `pctls` by the code; the stored files were not opened, because the peer engine does not read them.
