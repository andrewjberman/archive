# THREE_DATE_READ -- ADVI_COTBKF.TO-CB-bu-1 (round 73), 0.9.0_WK_ADVI_COTBKF~123

Read-only measurement; nothing was fetched. The rule was written to a file at **2026-10-11T19:24:25Z** before any comparison over the population and is copied in the record's `rule` key.

| group | funds | cells compared | equal same | equal before | equal after | funds by winner (same / before / after / undecided) |
|---|---|---|---|---|---|---|
| all | 101 | 944 | 794 | 744 | 579 | 17 / 15 / 0 / 69 |
| the nine | 9 | 93 | 45 | 88 | 32 | 0 / 6 / 0 / 3 |
| the rest | 92 | 851 | 749 | 656 | 547 | 17 / 9 / 0 / 66 |

Convention under the rule: **undetermined** (32 decided funds; one third of the population is 33.67). Without that clause: **no_single_convention**.

Sizing: validated 42, adjusted 21, not adjusted 21, undecided 0, not validated 59 (sum 101 of 101 funds). Substituted control: 20 validated, all read not adjusted. Differences from rounds 71 and 72: 0. Reach (floor): 267011 priced holding account-days, 1874 measured account-days.

**Headline.** Over 101 funds (944 compared reinvestment dates) the custodian's price equals the cached unadjusted close within 0.5 percent on the row's own date for 794, on the previous trading day for 744, on the next for 579; by fund 17 follow the same date, 15 the previous day, 69 are undecided (59 of them for fewer than 5 compared dates). The nine reproduce round 72 (93 cells: 45 / 88 / 32; 6 of 9 funds `before`, 3 undecided) but the other 92 funds do not behave as the nine: 17 same, 9 before, 66 undecided, and on the cells where only one date matches the nine are 39 of 39 `before` while the rest are 105 same and 77 before. Convention under the rule written first: `undetermined` (the 32 decided funds are under one third of the 101); with that clause removed it is `no_single_convention` (same 17, before 15; no kind, build-group or period split gives a class convention). Sizing: the cached close is validated for 42 funds; 21 read adjusted, 21 not adjusted, 0 undecided, 59 not validated (unsized); the 20 validated substituted funds all read not adjusted (control holds); 0 series differ from round 72 or round 71. Reach, a floor: 267011 priced holding account-days and 1874 measured account-days sit on dates where an adjusted fund's build close is below 0.98 of the cached close.

**Not established.**
- The posting convention is not established: the funds are split (same 17, before 15 among 32 decided) and 69 of 101 funds are undecided; 59 have fewer than 5 compared dates because the cache starts 2020-06-29 and most reinvestment rows precede it (791 of 1740 cells are outside the cache window). A fund-family or sponsor effect could not be tested: no sponsor field is on disk.
- Equal on all three dates for 458 of 944 cells: a fund's close often moves less than 0.5 percent over a day, so most cells cannot tell the dates apart; the winner rests on the minority of cells where they differ.
- The cached close validates a fund by matching the custodian price on at least one of the three dates on reinvestment dates (2020-06-29 on); that it is unadjusted for the fund's whole shared history is inferred from that match, not read date by date.
- The 59 unsized funds and the 121 with no cached close stay untested here: their round 71 reading (28 of the 59 read adjusted, 31 not adjusted) is neither confirmed nor refuted. The reach counts holdings that rest on a close below the cached close by more than 2 percent; it is not a return error and not a count of served wrong returns.
- An adjustment of under 2 percent over the whole shared window would read not_adjusted; ACTDX (the one non-substituted fund read not adjusted) has 70 shared dates only.
- Why the custodian row date relates to the vendor's bars as it does (ex-date, record date, pay date) is not read from any custodian field; the build close, the cache and the served files are the round 34 / 2026-10-09 vintages on disk; nothing was fetched.
