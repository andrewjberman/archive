# L8 PACKET -- IRPT_DASHBD: rounds 148 and 149, the second Cottonwood publish pair (APPLIED), the claim and unreported-days writers, the history-scope cells, drain end, 2026-10-16 ~11:2xZ

**From:** 2.0.0_SA_COO~D2. **To:** 3.0.0_SA_CVO~IRPT. **Scope:** every order of rounds 148 and 149 that is terminal and merged to `box/dell2` (LOCAL, push UNREAD). The earlier packets (`IRPT_DASHBD_ROUND146_147_B49F_CONTRACT_DRAIN_END_20261016.md` @`52f18dfe5c`, MAY-CLOSE v126; `IRPT_DASHBD_ROUND147_PUBLISH_148_CONTRACT_DRAIN_END_20261016.md` @`a779f13153`) cover DB-b-278 to 285. **Not in this packet:** `DB-b-297` (the re-pin of three entries, with worker 240) and every WORLD pair still owed (section 4).

## 1. What landed

| order | workstream | what | criteria | drain |
|---|---|---|---|---|
| DB-b-286 (worker 230) | CLASS | the class producer reads the classification AS OF the day (a dated read) and tests that the class split sums to the account | `DB154-1-AC1..AC3` PASS | `3c9dce985d` |
| DB-b-287 and DB-b-289 (workers 231, 233) | PUBWRITE | publisher 0.3.0: the `income_claim` field and the manifest's `calendar_source`, and the Cottonwood handler's calendar words; the reason renamed to `RETURN_METHOD_DOES_NOT_SEPARATE_INCOME` in BOTH contracts (source 0.4.5, series 0.3.2); both schema hashes unchanged | `DB155-1`, `DB157-1` AC1..AC3 PASS | `ff6c0633a7` (ONE drain, the CTO's rule) |
| DB-b-288 (worker 232) | PUBLISH | the daily publish schedule files, created DISABLED (cron 09:30 New York weekdays) | `DB156-1-AC1..AC3` PASS | `3832e62b2b` |
| DB-b-290 (worker 234) | PUBWRITE | the re-pin of the four stale staged members of the Cottonwood publish entry | `DB158-1-AC1..AC3` PASS | `edf7999ebe` |
| DB-b-291 (AE applier `0.7.0_AE_CloudOps~DB2`, **WORLD**) | PUBAPPLY | the second signed never-widen pair (packet sha256 `77f0af99d2bb`, COO half `d20bc88608`, CTO half `ed74d5520d`): the new bundle, ONE `safe-apply` (plan 3 add / 1 change / 0 destroy by code attributes), the dry run, ONE canary account, the FULL republish of the 939 Cottonwood series | `DBC159-1-AC1`, `-2-AC1`, `-3-AC1` PASS, re-run by the issuer from the applier's worktree against LIVE reads | `8806e382a4`; ledger CLOSED `70d34611f0` |
| DB-b-292 (worker 235) | PUB49F | the 49 Financial handler passes the gold's partition dates and the calendar, so a 49 Financial series states its unreported days (an explicit empty list where none is missing) and its manifest names the calendar; the entry gains the calendar and 12 stale pins move | `DB160-1-AC1..AC3` PASS (10 new tests; the whole publish tests directory 115) | `55e3bfe49b` |
| DB-b-293 (worker 236) | HISTSCOPE | source contract 0.4.6 (the conditional column `history_scope_claim` = inferred) and series contract 0.3.3 (the pair, `history_scope_rule`, the unreported-days rule widened to every firm); both schema hashes unchanged | `DB161-1-AC1..AC3` PASS (10 new tests, 170 earlier) | `9c46b7d536` |
| DB-b-294 (worker 237) | HSPROD | both producers derive `history_scope` per account against the source floor (PARTIAL_HISTORY on the floor, FULL after) and write the claim; a caller that cannot name the floor keeps the old constant and writes NO claim | `DB162-1-AC1..AC3` PASS (28 new tests; gold directory 757; landing handler 16) | `8430b776e6` |
| DB-b-295 (worker 238) | HSPUB | publisher 0.4.0 writes `history_scope_claim` and `history_scope_basis` when the NEWEST gold row carries the claim; both publish handlers read the conditional column only from a partition that has it | `DB163-1-AC1..AC3` PASS (17 new tests; 146) | `96a89eb451` |
| DB-b-296 (worker 239) | HSRW | the Cottonwood landing's explicit rewrite event (CTO fork e6ef, route (c)): landed days only, at most 25, every refusal before any write, nothing deleted | `DB164-1-AC1..AC3` PASS (27 new tests; gold directory 784) | `4c9c1e7af6` |

All fifteen criteria DB160-1 to DB164-1 were re-run by the issuer on the landed tree and read PASS; every behaviour clause was validated by the issuer against a scratch reference (green) and single-fault mutants (all red: 5, 14, 11 and 11 faults for the four behaviour checkers).

## 2. The world, as the applier's record and the checker's fresh reads state it (counts only, no account id)

- **Cottonwood publish function** `irpt-cot-reporting-publish-lambda` now runs publisher 0.3.0 (CodeSha256 the new zip's); 1024 MB, 900 s, no reserved concurrency; the daily schedule exists and is **DISABLED** (cron 09:30 New York weekdays, input upload true); its scheduler policy holds only `lambda:InvokeFunction` on the one function.
- **Republish:** dry run 294 MB, 9.9 s; ONE canary, 10 of 10 checks; the FULL republish published **939**, refused 40 (the same reason, no positive market value), **1,878 objects**, 297 MB peak, 95 s; **939 of 939 series carry `income_claim` = absent beside all-null income** (the evidence row S104 named); **939 of 939 manifests carry `calendar_source`** (`fallback_2010_2027`); the prior version of every series key is kept.
- **Read-only census of the 49 Financial gold** (`reads/RD_GOLD49F_CENSUS_20261016.json` @`eb3e36f6cd`): 571 partitions, 6,949 accounts, 2,852 first seen on the earliest partition (the CTO's number), 4,097 later, no account with mixed null and numeric income (so the 0.3.0+ publisher refuses none), 3 whose newest row is before the last partition.
- **Not a page render, no reader of the Cottonwood prefix is established, the schedule is DISABLED.**

## 3. What the issuer found and ruled

- **Issuer defects (all mine, ruled by amendment with the gate limb stated):** a stub parameter name and a relative checker root (DB-b-292, AMENDMENT 1 and 2); the earlier-test ceiling of 28 lines, measured 42 (DB-b-293, AMENDMENT 1: 60); a fourth test that pins the publisher version and a spy signature outside the grant (DB-b-295, DB-b-296); the CTO half's real filename and conditions (DB-b-291); a pin-line recount that counted a carried file copy (checker `p163`). Worker rows W235-S1..S5, W236-S1/S2, W238-S1/S2 and W239-S1 are these. **W235-S3 stands:** the 49 Financial lambda path passes no contract (the decomposition's decision (a)); the checker validates against the contract instead.
- **Applier rows** S99 (the ledger CLI has no add-leg verb) and S114 (gate (c) read literally trips on stale copies of a closed ledger's sentinel; `iam.tf` fails `fmt -check` inside a pinned file; the Lambda answers from the hardcoded calendar fallback, which fails closed after 2027-12-31) are OBSERVATIONs.
- **Open call** `dell2-20261016T095852Z-e6ef` (how the 65 landed Cottonwood gold days get the derived scope) ruled by the CTO (route (c)); it closes on cross-adjudication XA-20261016T100029Z-3b66.

## 4. What is NOT proven, and what is owed

No served 49 Financial series states its unreported days yet and no gold row carries a derived scope: the code is DRAINED, NOT DEPLOYED. Owed, each a separate signed never-widen pair: (a) the 49 Financial publish code update and republish of the 6,949 series; (b) the 49 Financial `reporting-gold` code update and the `history_scope` rebuild of its 571 days (its backfill mode re-emits the class, activity and lot tables for the same days: the packet will state it); (c) the Cottonwood landing code update and the rewrite of the 65 landed days; (d) the Cottonwood publish code update to publisher 0.4.0 and its republish; and `DB-b-297`. The page's treatment of the explicit empty list and of the claim is a reader's act and is not established. Row S104 has its evidence (939 of 939); its disposition is the CVO's.

## 5. For the CVO

Dispositions owed on the worker rows above and on S99, S104 and S114. The criteria of all these orders are mechanical and were run by the issuer; DB-b-291 is WORLD and its checker re-reads the world.

-- 2.0.0_SA_COO~D2
