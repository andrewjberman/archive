# L8 drain end -- ADVI_COTBKF round 74: the first return number (1,575 of 107,316 account-days change, for the validated funds only); 33 fund series validated unadjusted; the family split not established; 25 of 27 held series fetched; the correction list current

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~21:39Z | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB74bv1-AC2, CB74bv2-AC2, CB74bv3-AC2)
**Cut on:** `1.0.0_SA_CTO~DELL2` round-74 analysis @42390144c0. **Issued:** @2f22badbbf, 5 cells (3 at once; CB-bv-3 after CB-bv-2; the list last).
**Nothing was applied, served, re-minted or written to any bucket. One fetch was made, the one the analysis permits.**

| order | item | worker | state | issuer's own run at the drained base |
|---|---|---|---|---|
| CB-bv-1 | the date convention by fund family | ~127 | complete @1a47447419, drained | `FAMILY-SPLIT rule_written=True row=12/15+1/17 funds=101 families=2 family_funds=101 with_a_convention=1 reading=not_established against_family=1` |
| CB-bv-2 | the validation rule over 270 fund series | ~128 | complete @6abf9b3bef, drained | `VALIDATION-RULE rule_written=True minimum_dates=10 share_validated=0.8 share_refuted=0.3 fund_series=270 validated=33 refuted=0 unreadable=237 sum=270 changes_from_round_73=9 validated_not_distinguished=0` |
| CB-bv-3 | the first return number, built on a copy | ~129 | complete @83c486ce35, drained | `RETURN-CHANGE baseline_reproduces=True baseline_differing=0 validated_funds=33 securities_moved=19 other_securities_moved=0 account_days_compared=107316 changed=1575 under_1bp=1054 bp_1_to_10=425 over_10bp=96 band_sum=1575 measured_to_blank=0 blank_to_measured=8` |
| CB-bv-4 | the one permitted fetch (direct-act) | ~130 | complete @08bbd1d8c2, drained | `FETCH-HELD held=27 asked=27 asked_more_than_once=0 returned=25 empty=2 errors=0 outcome_sum=27 unheld_asked=0 bloomberg=False cache_before=3580 cache_after=3580 custodian_validated=0` |
| CB-bv-5 | the correction list brought current (direct-act) | ~131 | complete @715e50c106, drained | `OPEN-CORRECTIONS-RECORD revisions=4 record_absent=0 return_change=True floor=19 ceiling=NOT_MEASURED corrections=6 keys_complete=True dividend_evidence_rows=16 unreconciled=24` |

No product code changed in this round (the five drains carry records and channel rows only), so the suite was not re-run: it stands
at `1020 passed, 12 skipped` from round 73's code drain.

## 1. For L9: CB74bv3-AC2 (the first return number)

**The number, for the validated funds only.** Of 107,316 account-days measured in both builds, **1,575 daily returns change** when the
validated unadjusted close replaces the price now used: 1,054 by under 1 basis point, 425 by 1 to 10, 96 by over 10. 0 account-days go
from measured to blank; 8 from blank to measured. 30 of 82,593 month verdicts change (25 from DIFF to MATCH, 4 from UNGRADABLE to
MATCH, 1 from MATCH to DIFF).

**How it was made.** Both builds at the served pin under `method_r28`, into a worktree scratch. The baseline equals the served copy:
1,691,729 of 1,691,729 rows, 107,316 of 107,316 measured, 0 differing at a floor of 1e-12, and it equals the earlier pinned build of
round 68 (worker ~104's). The variant differs from the baseline in ONE input: a copy of the basis-census file in which 19 rows change class (18 from
`other`, one from `as_traded`, to `dividend_adjusted`), so the build's own as-traded basis substitutes the cached close for those 19.
The census path is a module constant with no flag (row D2-W129-S1); both builds ran through one scratch wrapper that sets it, and no
product file was edited. Moved: the 19 validated funds left on the store and no other security (34,277 security-days differ; 60
dropped by the basis's own bracketing rule). The control: the 14 validated funds already substituted moved on 0 of 26,507
security-days.

**The issuer's own read** (own script over the served copy and the worker's two builds): served against baseline 0 differing of
107,316; baseline against variant 1,575 changed, in bands 1,054 / 425 / 96, 8 measured in the variant only, largest 882.0 basis
points. Equal to the record. The issuer did not rebuild either build.

**For the grade:**
- **Only 5 of the 19 moved funds sit on a measured account-day** (FCNTX 792, BALCX 422, CWGIX 361, ANCFX 312, CAIBX 49; 361
  account-days hold two). The other 14 move no measured return. And 237 of 270 fund series are not validated at all: this is not the
  size of the defect.
- **Two things the record does not explain.** The largest change is 882.0 basis points on 2025-10-24 on an account-day holding FCNTX
  (the next are 881.7 and 216.2). And the variant return is HIGHER than the baseline on 828 of the 1,575 and lower on 747, where a
  dividend adjustment alone would be expected to lower returns across distribution dates; only 20 of the 1,575 fall on a custodian
  posting date of a distribution. The basis's own re-derivation rules act on a newly substituted fund together with the price, as the
  order's blind statement said. No cause is given for any single change.
- It compares one build with the other. It does not say which price is right.
- The price stores were re-read from the bucket today and are not pinned; the baseline equals served exactly, so this did not reach
  a return.
- `validated_funds` in the record is 33 (the validated population); 19 is the count that moved.

## 2. For L9: CB74bv2-AC2 (the validation rule)

The rule was stamped 20:31:42Z, before the run: a date is compared when the cache has the row's own-date bar and the previous bar; it
matches when the custodian's price equals the cached unadjusted close on either; **validated = at least 10 dates and 0.80 matching;
refuted = at least 10 dates and 0.30 or fewer matching.** The worker's reasons for each number are in the record and rest on accidental
match rates, not on yield. Over 270 fund series: **33 validated, 0 refuted, 237 unreadable** (121 no cached close; 48 no reinvestment
row; 68 fewer than 10 dates). By group: 19 of the 197 left on the store, 14 of the 73 substituted, 7 of the nine (AMCPX and NEWFX fall
under the minimum with every one of their 4 and 3 dates matching).

**For the grade:**
- **The adjusted close cannot pass for the unadjusted one here:** it also matches on 19 of 944 compared dates; all 33 validated funds
  have at least 10 distinguishing dates.
- Both days match on 598 of 944 dates: the rule validates a price level, not a date convention.
- 9 funds validated in round 73 on a 5-date minimum are unreadable here, each matching on every one of its 5 to 9 dates. A minimum
  of 5 gives round 73's 42; of 8, 37.
- Refuted is 0 under every threshold the worker tried: the refutation arm was never exercised on this population.
- Issuer's own check: the record's line and a recount of the 270-row list by group and reading (19 + 14 validated; 178 + 59 unreadable).

## 3. For L9: CB74bv1-AC2 (the family split)

The reviewer's row reproduces (12 of 15 day-before funds and 1 of 17 same-day funds are one family). The rule was stamped 20:32:11Z,
after that reproduction and before any family, pooled, held-out or rival count. **Reading: `not_established`.** One family reads
`before` (30 funds; decided 1 same and 12 before; pooled 102 before-only cells to 18 same-only over 25 funds); every other family has
1 to 3 funds and reads not established, for too few funds and not for being mixed. One fund sits against its family (CMLAX).

**For the grade:**
- **The held-out test does not confirm the family:** on its 17 undecided funds, 15 before-only cells to 10 same-only (0.60; the rule's
  line is 0.75).
- **Family and share class cannot be told apart:** share class read from the description classifies the 32 decided funds as well as
  family does (0.875), and all 13 decided funds of the A, F, C and 529 classes are in the one family. Inside it, post hoc and marked
  as a lead: the 529-plan funds are 10 same-only to 0, the A and F funds 15 before-only to 0.
- No pricing rule is proposed, per the ruling that the convention belongs to the validation.

## 4. The fetch (direct-act; no judgment criterion)

27 tickers counted and listed at 20:31:30Z, before the first request; each asked once of the source the cache already uses, by the
call the cache was built with; 25 returned 1,579 rows each, 2 were empty (CEM, FPNIX) and were not retried; no unheld ticker and no
other vendor was asked. The files are in a NEW folder beside the cache; the issuer counted the cache at 3,580 files and the new folder
at 25. All 25 read `looks unadjusted` against the build's close; **none is custodian-validated**, since none has a reinvestment row.
One outlier, VBTLX, has a lowest ratio of 0.18: the issuer's row D2-S126, not investigated. The library may retry internally and has
no switch for it; the worker says so.

## 5. The correction list (`deliverables/OPEN_CORRECTIONS.json`, revision 4)

The fund-basis entry keeps floor 19 and ceiling `NOT_MEASURED`, marks the three reaches as holdings counts and not return errors,
and holds the return number with its caveat in the same cell, the validation rule and counts, the family reading, and the fetch.
The re-mint mode carries the CTO's line as OWED by the pair: one conditional write against a scratch key in the real bucket before the
first real write. 24 unreconciled items, three new: 42 against 33 validated funds; the 882 basis points and the 828 higher returns, as
an open question; VBTLX. No PRD addendum past v0.7 exists.

## Where this leaves the project

- **In returns, for the 33 validated funds:** 1,575 of 107,316 measured account-days change, 96 of them by over 10 basis points.
- **Not measured:** the 237 fund series not validated (121 with no cached close, of which 25 now have an unvalidated fetched close).
- **Not decided here, the CTO's:** the fund-basis rule as a PRD addendum; what explains the 882 basis points and the direction of the
  changes before any of this is called a correction; whether the minimum is 10 or 5 dates; the VBTLX stretch; the addendum for the
  2022 factor; when the list closes.
- No re-mint order is cut. The served table is `method_r28`'s. The tree's default is `method_r29`.

**Round-close check:** REFUSED until the three judgment criteria are graded.
