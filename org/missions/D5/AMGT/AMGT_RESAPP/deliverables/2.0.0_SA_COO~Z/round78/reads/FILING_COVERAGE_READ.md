# READ 1 -- filing coverage: the 83 covered names with no filing analysis

Read for `2.0.0_SA_COO~Z`, AMGT_RESAPP round 78, 2026-10-07. Ruling: `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULINGS_AMGT_RESAPP_ROUND78_CALLS_AT_THE_CUT_20261007.md`, "What the two counts of section A change". Workspace HEAD at the read `3366536af5`. Script: `round78/checks/r78_read_filing_coverage.py`; its literal output `round78/reads/filing_coverage_read_output.txt`; every row `round78/reads/FILING_COVERAGE_READ.json`.

## The answer in three lines

1. **The "no cik" reason is an old marker, not today's state.** All 41 markers were written on 2026-09-17 from the 2026-09-16 universe. Today a CIK is stored for 21 of the 41: for 20 (every US ticker) it is already on the newest universe row, and for 1 (992 HK) Bloomberg's CIK sits in the pool list and the universe never reads it. The other 20 are non-US names nobody has asked Bloomberg about.
2. **The 42 stop before the first fetch.** All 42 first appear in the 2026-10-06 universe and the filing step has not run since 2026-09-22: 0 of 42 hold any marker, source object or silver row. 25 stop at the CIK (24 of them hold a Bloomberg CIK in the pool list that the universe does not read) and 17 stop at the FORM.
3. **The form is the wall behind both counts.** The newest universe decides a filing form for 12 of 95 covered names, and those 12 are exactly the 12 names that have an analysis. For the other 37 names with a CIK the row reads form "none", because the stored SEC ticker table holds no filing history.

## Where the filing step reads its CIK, and why it misses a stored one

| step | code | what it reads |
|---|---|---|
| the universe row's CIK | `lib/research/identity/build_universe.py:578-636` `filing_identity_for` | ONLY the stored SEC ticker table, looked up by the ticker's first part (`:589-590`). `build_union` hands it the pool record's key, exchange and folder (`:786-791`) and never the record's own `identity.cik`. |
| the form | same function, `:605-617` | the table's EDGAR filing history per CIK. The stored object is the SEC's raw ticker list, which has none (`_project_raw_sec_list`, `:498-516`, `submissions.unmeasured`), so the form is written as the text "none". A name keeps a form only from an older universe (`keep_prior_filing_form`, `:731-758`). |
| the plan | `lib/research/filings/batch.py:171-184` `plan` | ONLY the universe row's `filing_identity`. A row without `source: edgar` and a cik gets the reason at `:182`: "filing_identity.source is %r: no cik and expected form to fetch by". That is the sentence the page serves. |
| the marker | `lib/research/harvest/filings.py:369` `state_put_filing_attempt` | written once per name to `amgt/harvest/state/filing_attempt/security_key=<name>/UNRESOLVED-SOURCE.json`. |
| the page | `lib/research/api/scoped_amgt.py:3666-3669` | when no drafted document is stored, the marker's `reason` replaces the page's reason. No marker: the page says "no drafted document at ...". |

Three misses follow from that, each measured below:
- **The marker is never refreshed.** The local batch task `OpalResearch-FilingsAnalyzer` reads Disabled, last run never (`schtasks /Query`, this session). The newest marker in the store is dated 2026-09-22T03:31Z (180 objects), the day the markers were moved to their present address; their own `retrieved_at` is 2026-09-17.
- **Bloomberg's CIK is stored and unread.** The pool list record carries `identity.cik` and `identity.sec_id` for 65 of 243 records (from `CENTRAL_INDEX_KEY_NUMBER` in the identity bronze). The universe builder does not read it. The only code that does is the battery (`lib/research/filings/battery.py:491`), which the batch does not call (`batch.run_group` calls `fetch.build_source_object`, `batch.py:403`).
- **A ticker with a slash misses the table.** `BP/_LN_Equity` is looked up as `BP/`; the table's row is `BP` ("BP PLC", CIK 313807). Same shape for `NG/` (there the table's `NG` is a different company, NovaGold).

Read from the code and NOT run: `batch.plan` accepts the 37 rows whose form is the text "none" (the test at `batch.py:173` is truthiness), and `fetch.latest_filing` (`lib/research/filings/fetch.py:137-145`) would then look for a filing whose form equals "none" and find none. So a re-run of the batch today would turn "no cik" into "no none in the issuer's recent window" for those names; it would not fetch them.

## The denominators

| | names |
|---|---|
| covered names (`covered_security_keys()`), every `/thesis` 200 | 95 |
| no `.analysis.json` stored under `filings/v1/<name>/` | 83 |
| of those, the page's reason carries "no cik" (PART A) | 41 |
| of those, the page's reason opens "no drafted document" (PART B) | 42 |
| any other reason | 0 |

Stored places read: pool list `s3://opal-data-harvest/crosswalk/v1/2026-10-07.json`; universes `universe/v1/2026-09-15.json`, `universe/v1/2026-09-16.json`, `universe/v1/2026-10-06.json`; SEC ticker table `sec/harvest/bronze/company_tickers/date=2026-09-22/company_tickers.json` (10459 rows; the only SEC table under `sec/`); `identity/` holds one object, `identity/v1/2026-09-17-coverage-residue-crossref.json`, which is not a ticker table; `lib/research/identity/registrations.json` (72 registrations); the identity bronze (68 objects).

Newest universe (`universe/v1/2026-10-06.json`), source / form over its 302 rows: {"edgar / 10-K": 7, "edgar / 20-F": 6, "edgar / none": 163, "none / none": 126}. Over the 95 covered names: {"edgar / 10-K": 7, "edgar / 20-F": 5, "edgar / none": 37, "none / none": 46}.

## PART A -- the 41 names reading "no cik"

| class | names | what it means |
|---|---|---|
| CIK_IN_NEWEST_UNIVERSE | 20 | the newest universe row carries `source: edgar` and a cik; the served reason is the 2026-09-17 marker. All 20 are US tickers. The form is decided on 0 of 20. |
| CIK_STORED_NOT_IN_UNIVERSE | 1 | Bloomberg returned a CIK (pool list, registrations.json, identity bronze); the universe row carries none because the SEC ticker table has no row for the ticker. |
| ASKED_BLOOMBERG_NO_CIK | 0 | Bloomberg was asked and returned none, and no other place holds one. |
| NEVER_ASKED | 20 | no stored place holds a CIK and no identity bronze object exists: the name is in the pool list from its research folder and was never registered through Bloomberg. All 20 are non-US listings. |
| sum | 41 of 41 | |

CIK held, by place, over the 41 (a name can be in several): pool list 20; registrations.json 20; identity bronze 20; universe 20; SEC ticker table 20; SEC ticker table (same ticker text, not a US listing: not counted) 5.
First universe each name appears in: {"universe/v1/2026-09-15.json": 21, "universe/v1/2026-09-16.json": 20}. Marker `retrieved_at` day: {"2026-09-17": 41}.

| name | class | CIK | stored where | newest universe row (source / cik / form) | Bloomberg |
|---|---|---|---|---|---|
| 2317_TT_Equity | NEVER_ASKED | none | nowhere | none / cik None / form none | never asked |
| 9433_JP_Equity | NEVER_ASKED | none | nowhere | none / cik None / form none | never asked |
| 992_HK_Equity | CIK_STORED_NOT_IN_UNIVERSE | 932477 | pool list; registrations.json; identity bronze | none / cik None / form none | asked, CIK returned |
| AMD_US_Equity | CIK_IN_NEWEST_UNIVERSE | 2488 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 2488 / form none | asked, CIK returned |
| BBSE3_BZ_Equity | NEVER_ASKED | none | nowhere | none / cik None / form none | never asked |
| BP/_LN_Equity | NEVER_ASKED | none | SEC ticker table (same ticker text, not a US listing: not counted) | none / cik None / form none | never asked |
| BZLFY_US_Equity | CIK_IN_NEWEST_UNIVERSE | 1072397 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 1072397 / form none | asked, CIK returned |
| CPA_US_Equity | CIK_IN_NEWEST_UNIVERSE | 1345105 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 1345105 / form none | asked, CIK returned |
| ENEL_IM_Equity | NEVER_ASKED | none | nowhere | none / cik None / form none | never asked |
| GOOGL_US_Equity | CIK_IN_NEWEST_UNIVERSE | 1652044 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 1652044 / form none | asked, CIK returned |
| HSBA_LN_Equity | NEVER_ASKED | none | nowhere | none / cik None / form none | never asked |
| ICICIBC_IN_Equity | NEVER_ASKED | none | nowhere | none / cik None / form none | never asked |
| IDXX_US_Equity | CIK_IN_NEWEST_UNIVERSE | 874716 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 874716 / form none | asked, CIK returned |
| IMB_LN_Equity | NEVER_ASKED | none | nowhere | none / cik None / form none | never asked |
| ISRG_US_Equity | CIK_IN_NEWEST_UNIVERSE | 1035267 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 1035267 / form none | asked, CIK returned |
| KPN_NA_Equity | NEVER_ASKED | none | nowhere | none / cik None / form none | never asked |
| LLY_US_Equity | CIK_IN_NEWEST_UNIVERSE | 59478 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 59478 / form none | asked, CIK returned |
| MA_US_Equity | CIK_IN_NEWEST_UNIVERSE | 1141391 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 1141391 / form none | asked, CIK returned |
| MELI_US_Equity | CIK_IN_NEWEST_UNIVERSE | 1099590 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 1099590 / form none | asked, CIK returned |
| MNST_US_Equity | CIK_IN_NEWEST_UNIVERSE | 865752 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 865752 / form none | asked, CIK returned |
| NFLX_US_Equity | CIK_IN_NEWEST_UNIVERSE | 1065280 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 1065280 / form none | asked, CIK returned |
| NG/_LN_Equity | NEVER_ASKED | none | SEC ticker table (same ticker text, not a US listing: not counted) | none / cik None / form none | never asked |
| NOVN_SW_Equity | NEVER_ASKED | none | nowhere | none / cik None / form none | never asked |
| NOW_US_Equity | CIK_IN_NEWEST_UNIVERSE | 1373715 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 1373715 / form none | asked, CIK returned |
| QXO_US_Equity | CIK_IN_NEWEST_UNIVERSE | 1236275 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 1236275 / form none | asked, CIK returned |
| RKT_LN_Equity | NEVER_ASKED | none | SEC ticker table (same ticker text, not a US listing: not counted) | none / cik None / form none | never asked |
| RMS_FP_Equity | NEVER_ASKED | none | nowhere | none / cik None / form none | never asked |
| ROG_SW_Equity | NEVER_ASKED | none | SEC ticker table (same ticker text, not a US listing: not counted) | none / cik None / form none | never asked |
| RWE_GR_Equity | NEVER_ASKED | none | nowhere | none / cik None / form none | never asked |
| SPOT_US_Equity | CIK_IN_NEWEST_UNIVERSE | 1639920 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 1639920 / form none | asked, CIK returned |
| SSE_LN_Equity | NEVER_ASKED | none | nowhere | none / cik None / form none | never asked |
| ST_SP_Equity | NEVER_ASKED | none | SEC ticker table (same ticker text, not a US listing: not counted) | none / cik None / form none | never asked |
| TSM_US_Equity | CIK_IN_NEWEST_UNIVERSE | 1046179 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 1046179 / form none | asked, CIK returned |
| UBER_US_Equity | CIK_IN_NEWEST_UNIVERSE | 1543151 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 1543151 / form none | asked, CIK returned |
| ULVR_LN_Equity | NEVER_ASKED | none | nowhere | none / cik None / form none | never asked |
| UNH_US_Equity | CIK_IN_NEWEST_UNIVERSE | 731766 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 731766 / form none | asked, CIK returned |
| UNVGY_US_Equity | CIK_IN_NEWEST_UNIVERSE | 1890126 | universe; SEC ticker table | edgar / cik 1890126 / form none | asked, no CIK (Field not applicable to security) |
| V_US_Equity | CIK_IN_NEWEST_UNIVERSE | 1403161 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 1403161 / form none | asked, CIK returned |
| WALMEX*_MM_Equity | NEVER_ASKED | none | nowhere | none / cik None / form none | never asked |
| WDAY_US_Equity | CIK_IN_NEWEST_UNIVERSE | 1327811 | pool list; registrations.json; identity bronze; universe; SEC ticker table | edgar / cik 1327811 / form none | asked, CIK returned |
| ZURN_SW_Equity | NEVER_ASKED | none | nowhere | none / cik None / form none | never asked |

Five of the 20 NEVER_ASKED names share ticker text with a row of the SEC table. One is the same company; four are not:

| name | the SEC table's row for that ticker text | what the universe row says |
|---|---|---|
| BP/_LN_Equity | CIK 313807, BP PLC | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker 'BP/' |
| NG/_LN_Equity | CIK 1173420, NOVAGOLD RESOURCES INC | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker 'NG/' |
| RKT_LN_Equity | CIK 1805284, Rocket Companies, Inc. | REFUSED COLLISION: the SEC ticker 'RKT' maps to CIK 1805284 'Rocket Companies, Inc.', which shares no significant name token with the coverage name 'R |
| ROG_SW_Equity | CIK 84748, ROGERS CORP | REFUSED COLLISION: the SEC ticker 'ROG' maps to CIK 84748 'ROGERS CORP', which shares no significant name token with the coverage name 'Roche ROG SW', |
| ST_SP_Equity | CIK 1477294, Sensata Technologies Holding plc | REFUSED COLLISION: the SEC ticker 'ST' maps to CIK 1477294 'Sensata Technologies Holding plc', which shares no significant name token with the coverag |

UNVGY_US_Equity is the one name of the 41 where the places disagree: the SEC table gives CIK 1890126 ("Universal Music Group N.V./ADR") and Bloomberg answered `CENTRAL_INDEX_KEY_NUMBER` with "Field not applicable to security".

### A foreign issuer that files nothing with the SEC

**No stored field decides it today.** `filing_identity.form_expected` was meant to (it is measured from the issuer's own EDGAR history) and reads "none" on 289 of 302 rows of the newest universe, US names included, because the stored table has no history. What the store does hold:
- Bloomberg's own answer. A registered name whose `CENTRAL_INDEX_KEY_NUMBER` came back "Field not applicable to security" has no SEC number at Bloomberg: 2 of the 83 (UNVGY_US_Equity in part A, ORA_FP_Equity in part B).
- A Bloomberg CIK does not say an annual report is filed: 1299_HK_Equity (AIA) holds CIK 1522877 and whether it files a 20-F is not in any stored object.
- For the 20 NEVER_ASKED names nothing is stored either way.
So the class "files nothing with the SEC" cannot be counted from the store. It needs each CIK's filing history (the SEC's submissions index, a fetch this read did not make) or a stored copy of it.

## PART B -- the 42 names reading "no drafted document"

Stages, in the order the code runs them: S1 CIK (the newest universe row carries `source: edgar` and a cik), S2 FORM (its `form_expected` is a form, not "none"), S3 SOURCE (a RESOLVED source object: `filing_source` silver or an old `filings/v1/*.source.json`), S4 ANALYSIS (`filings/v1/<name>/<accession>.analysis.json`), S5 DRAFT (`drafting/v1/<name>.json`).

| first stage with no stored object | names | US | not US | last stage that produced one |
|---|---|---|---|---|
| S1 CIK | 25 | 0 | 25 | none: the universe row exists and carries no filing identity |
| S2 FORM | 17 | 13 | 4 | S1 CIK |
| S3 SOURCE, S4 ANALYSIS, S5 DRAFT | 0 | 0 | 0 | |
| sum | 42 of 42 | | | |

- All 42 first appear in the 2026-10-06 universe ({"universe/v1/2026-10-06.json": 42}). Names with any filing-attempt marker, old source object or silver row: 0 of 42. No fetch was ever attempted for them, which is also why the page shows the store's "no drafted document" text and not a marker's reason.
- A CIK held outside the universe: {"S1 CIK | Bloomberg asked, no CIK": 1, "S1 CIK | CIK held in pool list+registrations.json+identity bronze": 24, "S2 FORM | CIK held in pool list+registrations.json+identity bronze": 17}.
- Of the 25 stopping at S1, the universe's own note reads "the SEC ticker-to-CIK table ... carries no ticker" for 19 and "REFUSED COLLISION" for 6. Two of the refusals are the same company under a different spelling: OMAB_MM_Equity (the table's CIK 1378239 equals Bloomberg's) and TTE_FP_Equity (879764 equals Bloomberg's).

| name | first stage with no stored object | newest universe row (source / cik / form) | CIK held elsewhere | where | the universe's note (S1 only) |
|---|---|---|---|---|---|
| 1299_HK_Equity | S1 CIK | none / cik None / form none | 1522877 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker '1299' |
| 8035_JP_Equity | S1 CIK | none / cik None / form none | 1555504 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker '8035' |
| 8306_JP_Equity | S1 CIK | none / cik None / form none | 1468017 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker '8306' |
| 8316_JP_Equity | S1 CIK | none / cik None / form none | 1022837 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker '8316' |
| 8766_JP_Equity | S1 CIK | none / cik None / form none | 1169486 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker '8766' |
| 939_HK_Equity | S1 CIK | none / cik None / form none | 1445474 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker '939' |
| ADBE_US_Equity | S2 FORM | edgar / cik 796343 / form none | 796343 | pool list; registrations.json; identity bronze |  |
| AI_FP_Equity | S1 CIK | none / cik None / form none | 1658392 | pool list; registrations.json; identity bronze | REFUSED COLLISION: the SEC ticker 'AI' maps to CIK 1577526 'C3.ai, Inc.', which shares no significant name tok |
| AMXB_MM_Equity | S1 CIK | none / cik None / form none | 1129137 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker 'AMXB' |
| AZN_LN_Equity | S2 FORM | edgar / cik 901832 / form none | 901832 | pool list; registrations.json; identity bronze |  |
| BATS_LN_Equity | S1 CIK | none / cik None / form none | 1303523 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker 'BATS' |
| BNP_FP_Equity | S1 CIK | none / cik None / form none | 1272025 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker 'BNP' |
| CDNS_US_Equity | S2 FORM | edgar / cik 813672 / form none | 813672 | pool list; registrations.json; identity bronze |  |
| CELH_US_Equity | S2 FORM | edgar / cik 1341766 / form none | 1341766 | pool list; registrations.json; identity bronze |  |
| CLX_US_Equity | S2 FORM | edgar / cik 21076 / form none | 21076 | pool list; registrations.json; identity bronze |  |
| CNR_CN_Equity | S1 CIK | none / cik None / form none | 16868 | pool list; registrations.json; identity bronze | REFUSED COLLISION: the SEC ticker 'CNR' maps to CIK 1710366 'Core Natural Resources, Inc.', which shares no si |
| GPN_US_Equity | S2 FORM | edgar / cik 1123360 / form none | 1123360 | pool list; registrations.json; identity bronze |  |
| GSK_LN_Equity | S2 FORM | edgar / cik 1131399 / form none | 1131399 | pool list; registrations.json; identity bronze |  |
| HEI_US_Equity | S2 FORM | edgar / cik 46619 / form none | 46619 | pool list; registrations.json; identity bronze |  |
| IBE_SM_Equity | S1 CIK | none / cik None / form none | 1360587 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker 'IBE' |
| ICT_PM_Equity | S1 CIK | none / cik None / form none | 1656958 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker 'ICT' |
| ISP_IM_Equity | S1 CIK | none / cik None / form none | 1374384 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker 'ISP' |
| JD_US_Equity | S2 FORM | edgar / cik 1549802 / form none | 1549802 | pool list; registrations.json; identity bronze |  |
| KOFUBL_MM_Equity | S1 CIK | none / cik None / form none | 910631 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker 'KOFUBL' |
| MER_PM_Equity | S1 CIK | none / cik None / form none | 1545858 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker 'MER' |
| ML_FP_Equity | S1 CIK | none / cik None / form none | 896076 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker 'ML' |
| MSCI_US_Equity | S2 FORM | edgar / cik 1408198 / form none | 1408198 | pool list; registrations.json; identity bronze |  |
| NESN_SW_Equity | S1 CIK | none / cik None / form none | 792990 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker 'NESN' |
| NKE_US_Equity | S2 FORM | edgar / cik 320187 / form none | 320187 | pool list; registrations.json; identity bronze |  |
| NOKIA_FH_Equity | S1 CIK | none / cik None / form none | 924613 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker 'NOKIA' |
| OMAB_MM_Equity | S1 CIK | none / cik None / form none | 1378239 | pool list; registrations.json; identity bronze | REFUSED COLLISION: the SEC ticker 'OMAB' maps to CIK 1378239 'Central North Airport Group', which shares no si |
| ORA_FP_Equity | S1 CIK | none / cik None / form none | none | asked, no CIK (Field not applicable to security) | REFUSED COLLISION: the SEC ticker 'ORA' maps to CIK 1296445 'ORMAT TECHNOLOGIES, INC.', which shares no signif |
| PWR_US_Equity | S2 FORM | edgar / cik 1050915 / form none | 1050915 | pool list; registrations.json; identity bronze |  |
| RIO_LN_Equity | S2 FORM | edgar / cik 863064 / form none | 863064 | pool list; registrations.json; identity bronze |  |
| SAN_FP_Equity | S1 CIK | none / cik None / form none | 1121404 | pool list; registrations.json; identity bronze | REFUSED COLLISION: the SEC ticker 'SAN' maps to CIK 891478 'Banco Santander, S.A.', which shares no significan |
| SHOP_CN_Equity | S2 FORM | edgar / cik 1594805 / form none | 1594805 | pool list; registrations.json; identity bronze |  |
| SLB_US_Equity | S2 FORM | edgar / cik 87347 / form none | 87347 | pool list; registrations.json; identity bronze |  |
| SNPS_US_Equity | S2 FORM | edgar / cik 883241 / form none | 883241 | pool list; registrations.json; identity bronze |  |
| TTE_FP_Equity | S1 CIK | none / cik None / form none | 879764 | pool list; registrations.json; identity bronze | REFUSED COLLISION: the SEC ticker 'TTE' maps to CIK 879764 'TotalEnergies SE', which shares no significant nam |
| UBSG_SW_Equity | S1 CIK | none / cik None / form none | 1610520 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker 'UBSG' |
| VIVT3_BZ_Equity | S1 CIK | none / cik None / form none | 1066119 | pool list; registrations.json; identity bronze | the SEC ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker 'VIVT3' |
| ZTS_US_Equity | S2 FORM | edgar / cik 1555280 / form none | 1555280 | pool list; registrations.json; identity bronze |  |

## What the filing step last wrote

| store | objects | newest |
|---|---|---|
| drafting/v1 | 12 | 2026-10-05T23:43Z |
| filing-attempt markers | 180 | 2026-09-22T03:31Z |
| filing_source silver (issuer-site) | 1 | 2026-09-22T03:31Z |
| filing_source silver (sec) | 1 | 2026-09-22T03:31Z |
| old filings/v1 | 208 | 2026-09-30T15:14Z |

The 12 names with a decided form on the newest universe are the 12 with an analysis: ASML_NA_Equity, BABA_US_Equity, BA_US_Equity, COST_US_Equity, HAL_US_Equity, HD_US_Equity, INTU_US_Equity, KMB_US_Equity, NU_US_Equity, PBR_US_Equity, SAP_GY_Equity, VLO_US_Equity.

## NOT MEASURED

- **Whether any name actually files an annual report with the SEC.** No request went to sec.gov. A stored CIK is a number, not a filing.
- **What a re-run of the batch would do.** `batch.plan` was called on the three stored universes (a pure function); nothing was fetched. The "form none" outcome above is read from `batch.py:173` and `fetch.py:137-145`, not exercised.
- **Whether Bloomberg's CIK is the right filer for a foreign listing.** The 24 Bloomberg CIKs of part B were compared with the SEC table only where the ticker text matched a row (5 names: 2 equal, OMAB MM and TTE FP; 3 different companies, AI FP, CNR CN and SAN FP). The other 19 were not checked against anything.
- **The 12 analysed names and the 10 NO_USABLE_TABLE names** are outside this read.
- **Why the SEC table stored on 2026-09-22 is the raw list** and not the projection with filing history that the 2026-09-15 universe was built from: not traced.
- **The old `filings/v1/` objects' bodies** were opened only for UNRESOLVED markers; none of the 83 has a resolved one, so none needed opening.
