# Hand-over -- IRPT_BCKEND ~PN (the Scope account feed) and ~PO (the Orion re-cut) to 2.0.0_SA_COO~N2

**From:** `2.0.0_SA_COO~P2` (dell2) | **To:** `2.0.0_SA_COO~N2` (new seat) | **Date:** 2026-10-15 ~23:3xZ, measured on box/dell2 at the commit that carries this file
**Under:** CTO ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_DELL2_IRPT_PARALLELIZE_WORKSTREAM_ASSIGNMENTS_20261015.md` Move 1 (msg 8739), on Andrew's go `ANDREW_DIRECT_20261015_231xZ_PARALLELIZE_IRPT_SUITE_GO.md`.
**Your write surface (the ruling):** `data/inf/manual_api/`, `infra/aws/terraform/inf-pipeline`, the feed's `opal-data-assets/orion/inflection/` prefixes. A file touched by me and by you is a ruling back to the CTO, never two issuers.
**Method and its limit:** every state below was read from the order files, the `.open_deploys/` entries and the surprise channel in the main tree at this commit; "not read" is said where it is true. I did not read every live worktree's `.open_deploys/` for this file (the CVO's per-artifact rule, msg 8750, asks the applier to do that before its own entry).

## 1. What is yours, what stays mine

- **Yours:** ~PN (the Scope account feed script and its tests: IB-pr-586, 587, 594, 599), ~PO (the Orion re-cut: IB-pr-552, 556, 559, 560, 565, 596, 600, 603), the Orion pair (a) and pair (b) with its ADDENDUMS 1 and 2, the Scope feed IAM pair.
- **Stays with me (~P2):** the holdings producer (~P), the refused publishes and the exemption (~PJ, ~PQ), the split returns (~PM), row S206.
- **In flight finishes under its current issuer (the ruling):** IB-pr-596 (below) stays issued by me. Only NEW cells cut under you.

## 2. Non-terminal orders in your workstreams (measured: 1)

| order | workstream, round | risk | holder | state |
|---|---|---|---|---|
| `task-orders/IRPT_BCKEND.TO-IB-pr-596.apply-scope-account-feed.md` | ~PO r6 | WORLD | `0.7.0_AE_CloudOps~IB2` | status `pending`. APPLIED 21:11Z (msg 8665): the script, `trading_calendar.py` and the sidecar are on `code/manual_api/`, the dispatch object is replaced by HEAD's file (1 row, 2 chain entries, 0 other lines). NOT yet graded: the first scheduled chain run (about 11:32Z, 2026-10-16) is the proof; IB2 reads it. I grade the order when IB2's record lands, then you cut the follow-on cells. |

Every other order tagged ~PN or ~PO reads `complete`: 11 of 12 counted in the order files (~PN: IB-pr-586, 587, 594, 599; ~PO: IB-pr-552, 556, 559, 560, 565, 600, 603); IB-pr-596 is the 12th. IB-pr-568 (pair (a)'s dated apply) is tagged ~PB, not ~PO, and reads `complete`; IB-pr-550 (~P) and IB-pr-579 (~PI) are reads and applies of other lanes and read `complete`.

## 3. Signed pairs and ledger state

| pair | files (under `deliverables/2.0.0_SA_COO~P2/` and `deliverables/1.0.0_SA_CTO~DELL2/`) | applied by | ledger (`org/critical_paths/.open_deploys/`) |
|---|---|---|---|
| Orion pairs V3, pair (a) | `ORION_RECUT_PAIRS_PACKET_V3.md`, `NEVER_WIDEN_ORION_PAIRS_V3_COO_HALF.md`, CTO `NEVER_WIDEN_ORION_PAIRS_V3_CTO_HALF.md` | IB-pr-568 (the 33-day backfill; row S205) | applied; completion entry `20261015T0827Z_irpt-orion-33day-backfill-20261015_deploy_completion.md` |
| Orion pair (b) ADDENDUM 1 (the Scope account feed) | `ORION_PAIR_B_ADDENDUM_1_SCOPE_ACCOUNT_FEED.md` (blob 1e138cbeea), COO half `NEVER_WIDEN_ORION_PAIR_B_ADDENDUM_1_SCOPE_FEED_COO_HALF.md`, CTO half `NEVER_WIDEN_ORION_PAIR_B_ADDENDUM_1_SCOPE_FEED_CTO_HALF.md` | IB-pr-596 | `irpt-scope-account-feed-ib596-20261015.json` status OPEN: L1, L2, L3 CLOSED; **L4 OPEN** (the first scheduled chain run) |
| Orion pair (b) ADDENDUM 2 (the history backfill) | `ORION_PAIR_B_ADDENDUM_2_SCOPE_FEED_HISTORY_BACKFILL.md` (blob 73e7e712b7), both halves in the two folders | not read here whether an apply order exists or ran | no `.open_deploys/` entry named for it; **not read**: check the change-management folder and the decomposition sections 223 to 226 before relying on it |
| Scope feed IAM pair (+ ADDENDUM 1, spelling) | `NEVER_WIDEN_SIGNOFF_PACKET_SCOPE_FEED_IAM_PAIR.md` (blob cea5395ee7), `..._ADDENDUM_1_SPELLING.md` (blob f22b13a9), both halves in the two folders | IB-pr-600 (complete; I re-ran its three criteria, all PASS, and flipped it @860a9cdedd) | `irpt-scope-feed-iam-ib600-20261015.json` status OPEN with legs L1 to L6 all CLOSED (proofs present). The pair says the ledger closes on the issuer's word; I am giving it (msg to IB2 with this file) |

## 4. Open rows (the surprise channel, `surprise-channel/investigations/INVESTIGATION_v1.md`)

Owners are re-pointed to you by the appended row `IRPT_BCKEND-D2-S210` (this commit), not by editing the old rows. Read each row's own block and its latest disposition row (S189, S190, S191, S208, S209) before acting.

- **ARMED, owner ~P2, now yours:** `D2-W404-S4` (the chain's dispatch catalog existed only as an S3 object; IB-pr-596 L3 replaced it by HEAD's file, which does not by itself close the row: the CTO ruled it is brought into the repository by a later pair), `D2-W404-S6` and `D2-W409-S7` (T-1 completeness of the 06:00 New York flat keys is unmeasured; S191 names one owner), `D2-W404-S9` (the dispatch pull branch logs WARN and returns success when a pull step fails).
- **ARMED, no owner named in the row, read S190 first:** `D2-W409-S2` (the performance chain copy differs from the repository script; a positive control is owed before any performance day), `D2-W430-S3` (after the household lift `orion_selected.py` line 11 still states that the mapping refuses a multi-account household).
- **INERT, recorded (read before cutting):** `D2-W429-S1` to `S7` (default pull date rule, roster column name, two buckets, the chain's four synced prefixes, an unwritten partial envelope on a persistent 429, an unreachable branch, the rate limiter), `D2-W433-S1` to `S5`, `D2-W436-S2` (a skipped middle day is never rewritten by a scheduled rerun: the operator reruns with `--from-date`, written into the apply order and the first-run read, which fails the run on any SKIPPED line), `D2-W438-S1` to `S3`, `D2-W439-S1` to `S3`, `D2-S205`, `D2-S208`.
- **`D2-S209` (INERT):** the inf gold runner started for IB-pr-600's read is still running; the stop is ANDREW's act (CTO ruling msg 8597), queued as an open call. Not yours to stop.
- **Not counted here:** the many worker rows that read INERT and carry no hazard. The channel holds 1,267 row blocks in all; this hand-over lists the ones tied to your workstreams that I know carry an owner or an ARMED hazard, and I did not re-read every INERT row.

## 5. The follow-on cells already named for you

- After IB-pr-596's first run: the grade of IB-pr-596, then (the CTO's round analyses on `~PN`/`~PO`, `CTO_ROUND_ANALYSIS_IRPT_BCKEND_PO5_PS5_PY3_20261015.md` and the later ones in `org/tier1_exec/1.0.0_SA_CTO/deliverables/`) the Scope feed's history backfill (ADDENDUM 2) apply, if not already cut.
- The T-1 completeness measurement for W404-S6 and W409-S7 waits on a pair that moves `inf-gold-trigger` (V3 does not).

## 6. Records to read

Decomposition `org/missions/D9/IRPT/IRPT_BCKEND/decompositions/IRPT_BCKEND_DECOMP.md` sections 193, 195, 197, 198, 202, 218, 221, 223, 225, 226, 228 (your workstreams, in order); the L8 packets `deliverables/2.0.0_SA_COO~P2/IRPT_BCKEND_ROUNDS_*_P_DRAIN_END_*.md`; the CVO's per-artifact executor rule `org/tier1_exec/3.0.0_SA_CVO/deliverables/CVO_RULING_SINGLE_EXECUTOR_PER_ARTIFACT_20261015.md` (msg 8750): an apply on `inf-pipeline` state, an IAM role or the dispatch object runs in sequence with any other apply on the same artifact.

-- 2.0.0_SA_COO~P2
