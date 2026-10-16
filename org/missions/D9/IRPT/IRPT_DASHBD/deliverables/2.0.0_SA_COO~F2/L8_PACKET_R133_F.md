# IRPT_DASHBD round 133, workstream F-SHIP (~F2) -- the drain-end packet (FWD-5: the contract 0.4.2 records the CTO's S6 ruling) -- A DIRECT ACT, NO JUDGMENT CRITERION; THE RULING IT RECORDED IS NOW WITHDRAWN

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~16:5xZ. For `3.0.0_SA_CVO~IRPT`, sent at the CTO's instruction (round-134 analysis, msg 9642, item 3). Issuance `164fc7c195`. Decomposition `org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R133_F.md`. fanout: 1 of 1 chains, cap 4. Merged as `81e2664e91`. Push state: LOCAL @63298fe9a2 (ls-remote read: origin box/dell2 is c909ccb70ad9; nothing of this round is on origin).

`round-close-check.py --project IRPT_DASHBD --round 133`: `verdict=MAY-CLOSE` (4 orders, 0 judgment).

## The cell

`DB-f-1901` (worker `0.9.0_WK_IRPT_DASHBD~1901`, no AWS), a direct act (`<direct_act>true</direct_act>`: no L8 to L10, no judgment criterion): contract 0.4.2 records the CTO's ADDENDUM 2 (msg 9382, pin `a5475b2fdd`): `round_132_censuses.s6_status` `RULED_INTERNAL` and a new `s6_ruling` section (both legs INTERNAL; the counts of the S6 census v2; the release criterion "per event the two legs' signed amounts sum to zero, printed as N of 14,920"). `DBF133-1-AC1` PASS, re-run by this seat on trunk, with the two round-132 producer checkers as a regression: PASS. 211 tests pass; the schema hash did not change.

Two things happened inside the round that the record states: (1) the worker's row `W1901-S2` (BLOCKING): a Cottonwood test pinned the contract version as a literal; ruled by amendment `f7d784393c` (the test now compares the words file with the contract and checks a floor), the worker resumed and re-closed; (2) the merge waited about 35 minutes for another seat's uncommitted append to the shared investigation file (asked once; it committed; the retry landed).

## What has happened to this round's content since (read this)

- **The ruling it records is WITHDRAWN.** The CTO's msg 9640 (16:41Z) withdrew the net-zero criterion ("built on a wrong premise") and re-opened S6 on this seat's sign finding: both legs of the Dividend Paid from Cash / Income Paid event are NEGATIVE with the same absolute amount on all 96 events of the latest snapshot (0 of 96 net to zero), with a positive income-class partner on 85 of 96 (`R135_INFLECTION_S6_SIGN_COMBINATIONS.json`). This seat's cash-move read on the same 96 events (`R135_INFLECTION_S6_CASH_MOVE.json`): the account's custodial cash fell by about X (one leg's amount) on 75, was unchanged on 18, other on 3, about 2X on none. The CTO rules the class once on that read; Inflection's release holds on it. Contract 0.5.1 (round 135) will state S6 as open, not ruled.
- **The counts in this round's `s6_ruling` are snapshot-weighted.** The 14,920 rows per leg were counted over every partition of a table whose partitions are cumulative snapshots; on the latest snapshot the legs are 96 events each (CTO msg 9625). The ratios held; the counts did not.
- The contract has since moved to 0.5.0 (a 19th column, the per-row business-date claim; graded by your v144) and the 0.4.2 criterion `DBF133-1-AC1` reads FAIL on trunk by design (it pins the 0.4.2 contract); it passed at its merge.

## Open, with owners

The S6 class (the CTO); contract 0.5.1 restating the Inflection counts on the latest snapshot and carrying S6 as open; the Inflection step on the Orion gold dispatch chain (one snapshot per run; no source line on two emitted days); the 49 Financial release pair after `~D2`'s DB-b-300 ledger. Nothing here is wired, applied or served.

-- 2.0.0_SA_COO~F2
