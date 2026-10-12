# VALIDATED_UNADJUSTED -- round 74, TO ADVI_COTBKF.TO-CB-bv-2 (0.9.0_WK_ADVI_COTBKF~128)

Read-only measurement. Nothing was fetched; no code, test, config or manifest changed. Record: `VALIDATED_UNADJUSTED.json`; machine table of all 270: `VALIDATED_UNADJUSTED.csv` (the `reading` column is exactly validated / refuted / unreadable).

## The rule, written before the run (clock 2026-10-11T20:31:42Z; full text in the JSON `rule.text`)

- Equal: within 0.5 percent. A date is compared when the cache has a bar on the row's own date and the fund's previous bar (within 5 calendar days). It MATCHES when the custodian price (median of the date's `dvr` rows, Amount / Quantity, shares >= 0.05) equals the cached unadjusted Close on the row's own date OR on the previous bar.
- `minimum_dates` N = 10: for a low-volatility fund the chance that an either-day close falls within 0.5 percent by accident is at most about one half; at 0.80 required, 5 dates pass by accident about 19 percent of the time in that worst case, 10 dates about 5.5 percent (under 1 percent for any fund whose chance per date is 0.3 or less).
- `share_validated` S = 0.80: a fund whose cache is the traded price still misses about 5 percent of dates (round 72, the nine); 0.80 allows four times that and still demands most dates agree.
- `share_refuted` R = 0.30: a fund whose true match rate is 0.80 shows 3 or fewer of 10 matching under 0.1 percent of the time, so a refutation (at least 10 dates, at most 30 percent matching) is positive evidence.
- Not distinguished: a validated fund with fewer than 3 distinguishing dates (the unadjusted Close matches and the Adj Close does not). Such a fund counts as validated, is listed, and is flagged.

## Result over 270 fund series

| | fund series | validated | refuted | unreadable |
|---|---|---|---|---|
| all | 270 | 33 | 0 | 237 |
| left on the store | 197 | 19 | 0 | 178 |
| substituted (control) | 73 | 14 | 0 | 59 |
| the nine (overlay) | 9 | 7 | 0 | 2 |

Unreadable reasons (sum 237): no_cached_close 121 (all in the 197); no_reinvestment_row 48; fewer_than_minimum_dates 68 (23 of them with no compared date); between_refuted_and_validated 0.
Of the 197: 121 no_cached_close, 26 no_reinvestment_row, 31 fewer_than_minimum_dates. Of the 73: 22 no_reinvestment_row, 37 fewer_than_minimum_dates. The nine: AMRMX, CWGIX, WGIFX, CPXIX, FINFX, AWSHX, WMFFX validated; AMCPX (4 dates compared, 4 matching) and NEWFX (3, 3) unreadable on the minimum.

Validated (ticker compared/matching/distinguishing): ACTDX 35/35/35, BALCX 10/10/10, AMRMX 11/11/11, CMLAX 12/12/12, MAMTX 40/40/40, ABNFX 50/50/50, CAIBX 13/13/13, CWGIX 11/11/11, WGIFX 12/12/11, CPXIX 17/17/17, DFIEX 16/16/16, DFCEX 16/16/16, DISVX 16/16/16, DFLVX 16/16/16, DFREX 12/12/12, FSKAX 13/13/11, FCNTX 12/12/10, ANCFX 11/11/11, FINFX 12/12/12, MEIIX 23/23/23, NEA 29/26/26, NHMRX 72/72/72, FLTRX 72/72/72, PTTAX 12/12/12, PRILX 14/14/14, PDBZX 74/73/73, VEIRX 13/13/12, VBIRX 40/40/40, VWIUX 63/63/63, VFIAX 23/23/23, VTSAX 11/11/11, AWSHX 11/11/11, WMFFX 12/12/12.

## Against round 73 (42 validated on the best single date, 944 cells)

The same 944 cells are compared here (dropping the next-bar requirement adds 0). 33 are validated in both; none is validated here only; 9 are validated in round 73 and unreadable here on fewer_than_minimum_dates, every date matching: AMCFX (6 compared), FSMAX (5), FSPSX (9), FSSNX (9), FXAIX (7), MISIX (8), NFFFX (5), PCBIX (8), SGIIX (6). None is refuted. With N = 5 the validated set equals round 73's 42.

## What the either-date rule could wrongly accept

Over 944 compared dates: 940 match on either day; 598 match on BOTH days (the test cannot tell which day); the adjusted close also matches on 19 dates (12 distinct calendar dates, none before 2021-12-03, all with the unadjusted close also matching); 921 dates are distinguishing. Inside the 33 validated funds: 804 dates, 800 matching, 548 both days, adjusted also matching on 6, 794 distinguishing. Every validated fund has at least 10 distinguishing dates; none has fewer than 3 and none has zero, so `validated_funds_not_distinguished` is empty and 33 of 33 are distinguished.

## Sensitivity (not the result)

Validated count: N 5 / S 0.7, 0.8 : 42; S 0.9 : 41. N 8 : 37, 37, 36. N 10 (the rule) : 33, 33, 32. Refuted is 0 at every N, S and at R 0.2, 0.3, 0.4, 0.5.

## Not established

See `not_established` in the JSON: the date convention itself (598 dates match on both days); the 121 with no cached close and the 48 with no reinvestment row; 791 reinvestment dates before the cache starts; the 68 with too few dates; that the build's own series equals the cache for any validated fund; that the refuted threshold works on an adjusted series (never exercised here).
