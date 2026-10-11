# IB-pr-429 AMENDMENT 2 -- the date-basis claim re-counted under the ordered rule (counts only)

Read only. Same source, anchor, price rule, tolerance and trading-day axis as the first count. 85 graded days, 2026-06-10 to 2026-10-09, 1,000 accounts. The same account-days were read: this run's old-rule totals equal IB-pr-429's file exactly (76,796 present; 45,247 own date; 425 prior close; 17,488 ungradeable; 13,636 nothing to grade).

**The four counts, 76,796 account-days.** UNGRADEABLE 42,967. ACCT_OWN_DATE 20,138. NOTHING_TO_GRADE 13,636. ACCT_PRIOR_DATE 55. They sum to 76,796.

**What moved against IB-pr-429's rule, from the same rows in the same pass.** OWN_DATE to UNGRADEABLE: 25,109 account-days. PRIOR_CLOSE to UNGRADEABLE: 370. Not-graded and ungradeable, kept: 17,488. Not-graded and nothing to grade, kept: 13,636. Any other move: 0. Check: 45,247 - 25,109 = 20,138; 425 - 370 = 55; 17,488 + 25,109 + 370 = 42,967.

**Serving rule.** Eligible 75,796 (present today and on the prior graded day; the account-days of the first graded day are not eligible, as before). Served 32,341. Blank 43,455, which is 57.332 percent. Blanks by reason: today UNGRADEABLE 42,211; yesterday UNGRADEABLE 1,169; today ACCT_PRIOR_DATE 55; yesterday ACCT_PRIOR_DATE 20. Of 999 accounts with eligible days: never served 382, always served 127, sometimes served 490.

**Beside v0.34's floor.** v0.34: at least 25.0 percent of 75,796 blank, at least 169 of 999 accounts never served. The same pass reproduces that floor under IB-pr-429's alternative (24.976 percent blank, 169 never served). Under the ordered rule: 57.332 percent blank (+32.4 points), 382 never served (+213).

**The kinds held by UNGRADEABLE account-days** (an account-day is counted under every kind it holds). OUTSIDE_ANCHOR 34,437. NO_CUSIP 8,472. NEITHER_CLOSE 923. NEGATIVE_POSITION 286. ANCHOR_NOT_LANDED 0 (no anchor partition of the 85 days, or of a prior day, is absent now). Ungradeable account-days holding more than one kind: 1,018. With no kind: 0. Combinations: OUTSIDE_ANCHOR alone 33,441; NO_CUSIP alone 7,957; NEITHER_CLOSE with OUTSIDE_ANCHOR 478; NO_CUSIP with OUTSIDE_ANCHOR 360; NEITHER_CLOSE alone 290; NEGATIVE_POSITION alone 261; all three of NEITHER_CLOSE, NO_CUSIP and OUTSIDE_ANCHOR 133; NEGATIVE_POSITION with OUTSIDE_ANCHOR 25; NEITHER_CLOSE with NO_CUSIP 22.

**Anchor landing order** (object LastModified, the daily order a scheduled producer would meet; not turned into claims). The anchor landed after the Cottonwood partition on 23 of 85 days; the Cottonwood partition landed after the anchor on 62.

**Cash-flagged priced rows outside the anchor.** Primary treatment, as IB-pr-429: such a row is cash, nothing to grade. 31,307 account-days hold one. If the row were instead OUTSIDE_ANCHOR, 19,809 of them would change claim to UNGRADEABLE (the rest are already UNGRADEABLE). The addendum does not say; the effect on serving was not re-counted.

**Sixth reason.** 1 row (Units zero, Market Value above zero, not cash-flagged) fits none of the five kinds and has no price. It sits in one account-day that reads UNGRADEABLE by its other rows, so no claim depends on it. Not fitted to a kind. A row is filed.

**Control.** A fixture of 4 days and 6 accounts with counts known by construction, read equal to planted, key for key. It includes the two repair cases: an account-day whose graded rows are on their own date and which also holds an ungradeable priced row reads UNGRADEABLE (IB-pr-429's rule read OWN_DATE); an account-day holding two kinds lists both. It also tests that a day whose anchor is not in hand reads ANCHOR_NOT_LANDED.

**Not measured.** The serving effect of the cash-flagged sensitivity. Value or balance weight of any blank. Whether a day's rows are right. Any gold producer, any anchor widening. The anchor's content for days after 2026-10-09. A claim per row; only per account-day.
