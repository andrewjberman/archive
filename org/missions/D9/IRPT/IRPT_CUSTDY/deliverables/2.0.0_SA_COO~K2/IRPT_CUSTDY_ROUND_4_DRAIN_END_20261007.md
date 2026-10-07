# L8 drain end -- IRPT_CUSTDY round 4

**Issuer:** `2.0.0_SA_COO~K2` (dell2) | **Date:** 2026-10-07 ~12:1xZ | **For:** `3.0.0_SA_CVO` (L8 compile; no JUDGMENT criteria)

Round 4 is the round-3 analysis's E1-E3 (`1.0.0_SA_CTO~DELL2` @ec25e39844), cut as one issuance @94e67927f5 (`fanout: 3 of 3 chains,
cap 8`) from `decompositions/IRPT_CUSTDY_DECOMP.round4.md`. Every order is terminal and merged on dell2; 0 linked IRPT_CUSTDY worktrees.

| order | worker | drain | proof | real run on dell2 |
|---|---|---|---|---|
| CU-d-3 (E3) suite green | ~11 | @e05799d167 | VALID: AC1 `SUITE ... passed=74 failed=0` | fixture re-pointed to `'none'` (still refused by the fixed ids.py); no skip/xfail |
| CU-d-2 (E2) directory gap | ~10 | @7361085932 | VALID: AC1 10 passed, AC2 `DIRECTORY-GAP advisor=matthew_gooch granted=18 not_in_directory=4 reported=14 all_reported=True` | the 4 NOT_IN_DIRECTORY accounts have no custodian key (NO_SCHWAB_KEY): counted, not reportable (W10-S1) |
| CU-d-1 (E1) SI anchor | ~9 (re-seated twice) | @208a3ceedf | VALID: AC1 25 passed, AC2 `SI-ANCHOR ... rule1=12 rule2=2 ... branch_a=12 branch_b=2 labels_ok=True`, AC3 `SUITE ... passed=110 failed=0` | below |

**CU-d-1 was amended three times by the issuer**, each recorded on the order: 1 (@2063cabae7, 1b @ce710b5144) granted the hop3 files and
added AC3 when retiring the 2024 floor turned round 3's hop3 tests red (ARMED W9-S3); 2 (@09f7e2ab87) carried the CTO's ruling on W9-S2
(msg 423: branches a/b/c); 3 (@021117b977) granted CU-d-2's test file when its `si_anchor=ABSENT` assertions went red against E1 (ARMED
W9-S4). Both armed rows were seams between parallel round-4 cells, disarmed by the issuer the turn they surfaced.

**The one real run at close** (HEAD 208a3ceedf, ~12:0xZ): `HOP3-REAL-RUN advisor=matthew_gooch as_of=2026-09-30 households=10 accounts=14
uncovered=4 held_si=0 not_in_directory=4 of=18 error=none`. From its file (not committed: client figures; row S9 carries the summary):
SI OK on 14 of 14 accounts and 10 of 10 households (round 3: 0 of 24); anchors rule 1 x12 labelled `since inception (first funded <date>)`,
rule 2 x2 labelled `since <date>, the first date Opal holds`; uncovered 4, all NO_SCHWAB_KEY. Drain checks on CLOUD: `py_compile` 10/10,
ruff clean, `SUITE ... passed=110 failed=0 errors=0 xfailed=1`.

**FWD-1 thread: NOT LIVE.** Hops 1-4 run on real data with figures complete for the advisor's covered accounts. Hop 5 waits on
IRPT_BCKEND a1-a4/E-P9 and on the template (the portal kit landed ~12:07Z, msgs 467/471: the round-3 E3 gate is now open and is being
issued); hop 6 is Andrew's.

## Rows of the round

| row | class | standing | note |
|---|---|---|---|
| W9-S1 | OBSERVATION | INERT | no `dim_account`; the custodian open date is `fact_acc.date_opened` |
| W9-S2 | OBSERVATION | INERT | rule-1 dates precede the first linkable return; RULED by the CTO (msg 423), carried as amendment 2 |
| W9-S3 | OBSERVATION | ARMED -> disarmed | hop3 tests red after the floor's retirement; amendment 1 |
| W9-S4 | OBSERVATION | ARMED -> disarmed | directory-gap assertions red against E1; amendment 3 |
| W9-S5 | OBSERVATION | INERT | branch (c) "holdings before Opal's first partition" cannot be read directly; implemented as holdings present or an unconfirmed zero read; no real account in (c); probe takes ~150 s |
| W10-S1 | OBSERVATION | INERT | the advisor's 4 NOT_IN_DIRECTORY accounts have no custodian key |
| S9 | OBSERVATION | GRADUATED | the round's close and real-run grade |

**For the round-4 analysis (not rows):** the 4 unkeyed accounts (does Schwab hold them under another key? IRPT_BCKEND's census, msg 413:
1,447 no bridge source, 482 xref unresolved, 32 absent-from-feed); IRPT_BCKEND's fixed `ids.py` still refuses lowercase `'none'`/`'NaN'`
(case-sensitive guard; 0 in the seam today); the probe's ~150 s run time.

-- 2.0.0_SA_COO~K2
