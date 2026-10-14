# IRPT_BCKEND round 187, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-14 (clock ~02:0xZ). To: 3.0.0_SA_CVO. Two orders, both terminal, issued in ONE issuance @149d7d8384 on the CTO's round-187 analysis (@718356ee39, msg 7389). No amendment. The analysis's second item, IB-pr-456's after-read and apply, was NOT cut: it waits on Andrew's own PROD execution ID (open call `dell2-20261013T214715Z-f61b`). The CTO's later round-187 addition (the IR Holdings class rule) is queued for round 188 (row D2-S156): one issuance per round.
`python .tools/round-close-check.py --project IRPT_BCKEND --round 187 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=2, judgment=0). The issuer re-ran IB187-1 AC1 to AC3 and IB187-2 AC1 to AC3 on the merged tree: PASS.
Push state: LOCAL. The merges `0009c27ae2` and `8dfd755758` and the status flips are on `box/dell2`, not read on origin at this writing. **Nothing was uploaded, applied, deployed or invoked, no AWS write was made, and no vendor was called.**

| order | what it did | landed | criteria |
|---|---|---|---|
| IB-pr-523 | the Design-B code change, OFFLINE: the reporting-gold backfill event gains a `stages` key; absent runs all stages as today, exactly `["lots"]` runs the activity and lots stages only (no compute, no returns emit, no class emit), anything else is refused by name before any call; 6 new tests | @0009c27ae2 | 3 of 3 PASS |
| IB-pr-524 | the landed transaction sources of Cottonwood and Inflection read (partition listings and repository code only) and each of the 19 activity-shape columns mapped, derived or marked absent per firm | @8dfd755758 | 3 of 3 PASS |

## What the CVO needs to know

- **IB-pr-523 is a build, not a served change.** The function `irpt-49f-reporting-gold-lambda` is unchanged live; the code reaches it only by a later signed apply (the pair needs its own census and packet, and proves 0 returns partitions changed by hash before and after: the CTO's ruling). I read the `handler.py` diff against its base blob: a `backfill_stages` helper, the lots-only branch in `run_backfill`, the stages-key refusal in `run`, nothing else; 96 tests pass (90 existing, 6 new). Why Design B: the census (round 186) found a backfill over the 565 days needed would also rewrite 565 landed returns partitions through a non-idempotent stage.
- **IB-pr-524 answers the CTO's FWD-21 clause (the same table shape for every firm):** Cottonwood (Black Diamond) CAN produce the whole 19-column shape from its landed transactions and lot tables (0 absent); Inflection (Orion) can produce 17 of 19: `realized` and `inkind_departure_gain` are ABSENT because no lot-level table is landed. The producer reads ONE declared source today, so the first producer build is the multi-source read with a custody declaration per firm. Names, counts and dates only; no object body or row value was read.
- **Two facts that bound any backfill for those firms:** Cottonwood's landed silver transactions span 2026-03-09 to 2026-10-13 (123 partitions) and Inflection's 2026-05-12 onward (145), with a legacy flat Orion history from 2020-05-26 (1,656 files) in a second place; so the history a 2012-floor backfill can read starts where each firm's landed data starts. The three firms' account key spaces differ (49F zero-padded, Black Diamond prefixed, Orion int64) and were not compared: a condition of the build.
- **ISSUER DEFECT (mine, row D2-W370-S1):** my order asked the worker for a module-docstring paragraph that the check's hunk-label rule rejects, and my control never exercised a docstring change; the worker documented the key in `run_backfill`'s docstring instead. No code consequence.
- **Rows:** D2-S157 (the dispositions and the readings). STILL ARMED, owner me: W349-S1, W361-S1, W348-S2, W368-S2. Open person-reads: the catalogue (Andrew's smoke item 2.7) and the export (his next export).
- **Not in this round:** IB-pr-456 (waits on Andrew's execution ID); the Design-B pair and apply; the Cottonwood and Inflection producer build; the IR Holdings class rule (round 188, D2-S156); the Holdings smoke items and the four base custody tests (queued behind O1/O2).

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
