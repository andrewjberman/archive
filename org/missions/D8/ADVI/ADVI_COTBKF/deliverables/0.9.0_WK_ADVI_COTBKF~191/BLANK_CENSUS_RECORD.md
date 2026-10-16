# BLANK-CENSUS record -- ADVI_COTBKF TO-CB-cx-1 (round 102, CB-cx-1)

Worker 0.9.0_WK_ADVI_COTBKF~191, read-only. Served versions: daily_returns lNzQMjfx6uX2zdFdWKsDANboShtDUz2N, month_grades nkTE.F82uFSboXr9PEamIENCwFL9cwcC, account_day_value ObKZXku7Am.QGjO.oSAsIScy8IcJxN5a. Machine record: `BLANK_CENSUS_RECORD.json` (same folder). Builder: `cx1_record_build.py`.

Issuer's census (`cx1_blank_census.py`, no argument), reproduced:

- CENSUS-DAYS total=1691729 with_return=107316 blank=1584413 unreasoned=0
- CENSUS-MONTHS total=82593 not_match=78915 unreasoned=0
- CENSUS-UNPRICED rows=15973399 cusips=4371 never_priced_cusips=3791 never_priced_rows=7492099 gap_cusips=580 gap_rows=8481300

CTO criterion (blank with no reason = 0, and non-MATCH months with no reason = 0): MET on the served tables.

## Days by reason (blank 1,584,413)

| Reason | Days | Bloomberg fill |
|---|---|---|
| UNPRICED | 1,558,187 | yes (missing close) |
| NON_POSITIVE_BASE | 22,521 | no |
| FIRST_DAY | 1,533 | no |
| DVR_CLOSE_STEP | 1,069 | no |
| HELD_SOURCE_UNDER_REVIEW | 988 | no |
| REGRESSED_UNDER_AS_TRADED | 110 | no |
| FLOW_UNVALUED | 5 | not established |

## Months (non-MATCH 78,915)

UNGRADABLE 78,622 (a month can carry more than one reason kind): blank-day clause 77,565 (first blank reason UNPRICED 74,791; NON_POSITIVE_BASE 1,173; FIRST_DAY 1,533; HELD_SOURCE_UNDER_REVIEW 47; DVR_CLOSE_STEP 21); no reported monthly return 1,901; reported span not one calendar month 2,865; no daily returns 116; reported rows disagree 15; reported value not finite 8. DIFF 288. ABSENT 5 (REGRESSED_UNDER_AS_TRADED). MATCH 3,678.

## UNPRICED holding-days (15,973,399 over 4,371 securities)

- Never priced: 3,791 securities, 7,492,099 holding-days. Gap: 580 securities, 8,481,300 holding-days.
- Never-priced by asset type (securities / holding-days): Mutual Fund 873 / 4,255,286; Equity 1,335 / 1,734,224; Fixed Income 764 / 808,211; ETF 143 / 189,810; Cash Equivalent 477 / 200,770; Mutual Fund (Closed End) 90 / 166,568; Annuity 29 / 83,370; Unit Investment Trust 58 / 40,350; Alternative Investment 22 / 13,510.
- Never-priced by ticker status (replay of the valuation's resolution on the round-99 cache; securities / holding-days): no ticker symbol 1,139 / 873,269; ticker with no store row 1,657 / 3,535,870; ticker key claimed by more than one security 98 / 749,593; resolved but security-days dropped as conflicting 82 / 243,571; resolved, no own conflict, still unpriced 815 / 2,089,796. The last two rows are approximate: the replay prices 897 never-priced cusips that the served as-traded basis does not.
- Gap, by position (securities with rows in the position / holding-days): before the first priced day 571 / 8,480,069; after the last 22 / 959; interior 27 / 272. A security can sit in more than one position.
- Bloomberg overlap: the committed request lists for Cottonwood (ZZ-ADVI_COTBKF-ACTIVE-BBG-01..27, MDPF_SECHIST-CARD-A-B1-OPTION-C, the COT-BBG-HISTORY ranked list) list 3,059 distinct cusips, of which 2,354 are never-priced and 515 gap. Whether they came back priced: not established (no committed record carries a per-security outcome; BBG_ACTUALS.jsonl holds job-level cell counts only).

## Cross-check

Account-days with an unpriced holding-day: 1,556,548 of the 1,558,187 UNPRICED blanks; the other 1,639 are the prior-day half of the rule.

## Not established

FLOW_UNVALUED split (price versus Quantity or CUSIP); the came-back count; the replay-versus-served basis difference (surprise rows ADVI_COTBKF-D1-W191-S1 to -S3); the no-daily-returns month kind. Nothing was filled, served or graded.
