# DSGN_AMGTV1 round 67 -- CLOSE (2.0.0_SA_COO~D1, dell1, 2026-10-09 ~15:4xZ)

| item | value |
|---|---|
| list | `ledger/ROUND_ANALYSIS.round66.md` section 2: item 1 FWD-8 (the peer table), item 2 FWD-27 (one format per measure) |
| issuance | @42b0206316, fan-out 1 of 1, LF only |
| order | `TO-AV-zzr-1` -> ~141 (worker). AMENDMENT 1 @f1bce3cf03 (rows D1-W141-S1/S2: the round22 `subjectrow.cjs` re-anchor granted). AMENDMENT 2 @3798de29d1 (the close walk 15:12Z showed the first build's MEASURED-or-name rule hiding real exchange tickers; the rule was corrected and r67's ticker arm amended). Drained @273e9845f8 and @326f0d3776 |
| checks on both candidates | r62 6/6, r63a 3/3, r63b 5/5, r63c 5/5, r64a 4/4, r65 4/4, r67 6/6; battery29 ALL PASS (0 skipped) |
| DEV | candidate `32835ce5` = origin DEV `2726bbe7` + `f21e60db` (the first build) + the cherry-pick of ~141's `45a957a9` (`cand/dsgn-amgtv1-r67-dev`) |
| PROD | candidate `a97e5dff` = PROD `18364342` (portal-v2.1.210) + the same two commits (`cand/prod-dsgn-r67`). 6 files changed, 0 of them outside `src/pages/SecurityAnalysis/`. The SA tree equals the DEV candidate's (empty diff). No PROD half is asked until the CVO grades AV-zzr-1. |
| rows | D1-W141-S1, D1-W141-S2 (ruled in AMENDMENT 1). Three producer rows to AMGT_RESAPP: `AMGT_RESAPP-D1-S14`, `-S15` and `-S16` (below). |

## The real run -- 15:33Z-15:38Z, `tmp/ui-walk/20261009T153310Z`, signed-in `dev:live` build of `32835ce5`

`--security ASML_NA_Equity --security 992_HK_Equity --security AMD_US_Equity`: 90 screenshots, 0 API issues, 0 guard aborts. The
walker disarmed, and its login is refused (401). An earlier attempt at 15:32Z was void: the walker could not arm, because the default
Python has no bcrypt. No page was read in it.

| criterion | shot | what it shows |
|---|---|---|
| FWD-8, tickers | 014, 042, 070 | Every peer with an exchange ticker shows it: INTC, CSCO, AMAT, ORCL, LRCX, AMD, NFLX, MU, PANW, DELL, AVGO, TXN, KLAC, APH, MRVL, ADI, QCOM. A peer whose served ticker is a SEDOL or an exchange number shows its name instead: Tencent, SK hynix, Foxconn Industrial Internet, Zhongji Innolight, Cambricon, Hygon, and ASML as a peer. No cell shows an internal id or a sentence. |
| FWD-8, currency | 014, 042, 070 | Every price and money cell carries a currency, or the words "currency not stated" where none is served. ASML's caps and EVs read "(local)" over EUR and USD cells. AMD's read "Mkt Cap (USD)" and "EV (USD)", since every cell there is USD. 992 HK's EV reads "(local)", because the subject's EV is served without a currency. The page computes no cross-currency figure. |
| FWD-8, coverage | 014, 042, 070 | All three names' peers are walked (12 comparables each). |
| FWD-27, price | 014 | ASML's price reads "EUR 1,626.20" in the tile and in the subject row: two decimals and one thousands rule in both. 992 HK reads HKD 32.84 in both, and AMD reads USD 620.68 in both. |
| FWD-27, market cap | 014, 042, 070 | The cap uses one unit and one label in the tile and the table: "EUR 631B, as of October 9th, 2026", "HKD 421B" and "USD 1.01T", each with the same date line. The earlier "EUR 541,932" mm figure is no longer on the page, because the subject cell reads the header's CUR_MKT_CAP. The two values differ in measure and date, which is producer row S15. |

## Seen, not graded here (for the round-67 analysis)

- 992 HK: the EV tile reads "--" (no CURR_ENTP_VAL served), while the subject row reads "60.91B currency not stated", which comes from
  the peer set. These are two sources for one measure: one absent, one without a currency. This is producer row S14's class.
- The summary rows: Price reads blank on Average and "--" on Median, Min and Max. The footnote explains the Average.
- `round64/PREP.md` items 1-3 are still carried.

## Producer rows filed (AMGT_RESAPP, `2.0.0_SA_COO~R1`)

- **S14:** peer prices are served with no `price_currency`. That is 10 of 12 peers on ASML, 11 of 12 on 992 HK and 12 of 12 on AMD.
  The same applies to 992 HK's subject EV.
- **S15:** the subject `market_cap_musd` reads 541,932 USD mm as of September 19th. The header's CUR_MKT_CAP reads EUR 631B as of
  October 9th. The peer set's cap is stale against the header.
- **S16:** most served peers are identity UNRESOLVED. Their `ticker` field holds a SEDOL or an exchange number where a non-US listing
  has an exchange ticker (Tencent 700 HK, SK hynix 000660 KS).
