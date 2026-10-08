# ETFS_RIVALS round 28 -- task-order packet for 3.0.0_SA_CVO~RV (CTO rulings R19, R20, R24; ROUND_ANALYSIS.round22 ADDENDUM 6)

**Compiler:** `2.0.0_SA_COO~RV`, 2026-10-08 ~20:xxZ. Issuance 222194aee0; AMENDMENT 1 to RIV-tc-1 @8d50ab6e32 (the cap
20,000, Andrew-direct via CTO msg 31926). Two orders, both terminal. Nothing deployed, nothing written to S3, no model or
vendor call by this round so far.

| cell | order file | state | mechanical criteria, re-run by the issuer |
|---|---|---|---|
| RIV-aw-1 | `ETFS_RIVALS.TO-RIV-aw-1.ai-accounts-name-periods-in-words-and-cite-every-figure.md` | complete, MERGED (branch tip a2283fc349) | aw-1.AC1 PASS 10 of 10, aw-1.AC2 PASS 10 of 10 |
| RIV-tc-1 | `ETFS_RIVALS.TO-RIV-tc-1.a-top-up-close-is-stored-with-a-currency-and-the-owed-window-ends-on-the-page-day.md` | complete ON ITS BRANCH `wk-ETFS_RIVALS-22` @b0b65368fb, NOT merged | tc-1.AC1 PASS 8 of 8; tw-1.AC1, tw-1.AC2 PASS (on the branch) |

Merged CLOUD: suite `919 passed, 3 skipped`; 40 of 42 check files end `PASS 0 failures`; the two others, tc-1.AC1 and
tw-1.AC1 (arm e, the cap 20000), grade the unmerged branch.

## The real runs J1 is graded on

- **RIV-aw-1 J1:** none yet, by design. The words are made by a model, and no seat calls it. The first real accounts under
  `a1-chain/7` are the first 13:00Z sweep after the round-28 Lambda deploy (a pair; the executor seat applies, ruling R22).
  The issuer then counts, over the 26 served account items: period codes (0 expected), items stating their two dates (26
  expected), FAIL items, the sum of `attached_figures` and of `corrections`.
- **RIV-tc-1 J1:** none, by design: the switch is unset and the merge waits on RIV-tw-1's J1 (the 2026-10-09 11:00Z
  vehicle run, C-S80), then a pair. The first scheduled vehicle run after the merge is the read.

## Rows of the round

- `ETFS_RIVALS-Z-W21-S1` (worker ~21): the grounding check read the 30 in "the last 30 days" as a figure; the worker
  exempted the three period phrases in `_figures`. Issuer: kept (the order asks for those words). It also loosens the
  re-grade of an older stored account that wrote such a phrase.
- `ETFS_RIVALS-Z-W21-S2` (worker ~21): a correction chat that raises leaves the first reply standing, graded FAIL with a
  wording reason. Issuer: kept.

## Stated, for the analysis

- `GRADER_VERSION` stays `grounding_check/6` (the new rules bind rows of `a1-chain/7` and later only).
- The budget record of the history-owed step is in points requested; with one date per request it is an upper bound of
  the returned records (CTO msg 31941: returned records is the ledger's unit). The switch-on pair names it.
- Still carried: R18 (row Z-S73); the day-early 2026-09-29 pull; `.tools/round-close-check.py` reads the first status
  tag (row Z-S77).
