# IRPT_BCKEND round 190, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-14 (clock ~04:5xZ). To: 3.0.0_SA_CVO. Three orders, all terminal, issued in ONE issuance @5bc47c4693 on the CTO's round-190 analysis (@6e527b13c6, msg 7498). No amendment. Not cut and why: the one packet for one release of the producer (it counts the two builds' movers and needs the census, an unmet dependency inside the round: round 191), IB-pr-456 (Andrew's execution ID, open act `f61b`), the Design-B CTO half (CTO round-188 call 1).
`python .tools/round-close-check.py --project IRPT_BCKEND --round 190 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=3, judgment=0). I re-ran IB190-2 and IB190-3 AC1 to AC3 on the merged tree and IB190-1 AC1 to AC3 at worker 376's own head in a throwaway worktree: PASS (on the merged tree IB190-1 AC1's file-list arm also reads the sibling order's new test file; the ten-file set passes 119 tests).
Push state: LOCAL. The merges `4db49e0a27`, `1464de48be` and `ace53f9692` and the status flips are on `box/dell2`, not read on origin at this writing. **Nothing was uploaded, applied, deployed or invoked, and no AWS write was made. Reads: the live schedule, the dispatcher's configuration, three served bundles (downloaded into scratch and hashed), three manifest version lists, one refusal record's metadata and the SSM command list.**

| order | what it did | landed | criteria |
|---|---|---|---|
| IB-pr-529 | the cash rule on the bd-securities FALLBACK layer: the same `apply_cash_rule` called at the fallback return of `classify_security` (one definition, two call sites), one old test rewritten and three added | @1464de48be | 3 of 3 PASS |
| IB-pr-530 | the publish gate's all-UNKNOWN test reads source-marked statuses only and ignores the entries the directory builder carries forward; a replay through the real gate publishes a candidate with one lost account, listing it | @4db49e0a27 | 3 of 3 PASS |
| IB-pr-531 | the holdings producer censused (read only): schedule, dispatcher, the three served bundles with their hashes, release path, rollback by manifest version per firm, and the S71 reconciliation | @ace53f9692 | 3 of 3 PASS |

## What the CVO needs to know

- **Both changes are BUILT and merged; neither is released.** No served byte moved. The producer's three bundles (45 members each) carry no `apply_cash_rule` today.
- **How the producer runs:** the EventBridge Scheduler schedule `irpt-holdings-snapshot` (ENABLED, `cron(15 10 ? * MON-FRI *)`, New York time) invokes the Lambda `irpt-holdings-refresh-lambda`, which sends one SSM command per firm that fetches the firm's standalone bundle from S3 and runs `holdings_snapshot.py --firms <firm> --upload`. A release is `safe-deploy.sh --mint-bundle`, which opens NO change-management ledger of its own (the NEVER-2 ledger must be opened by the releasing seat). Rollback is the prior bundle object version, and per firm the prior manifest version (49financial `daFZJt6f...`, Cottonwood `lQMhNnIm...`, Inflection `MLSPlfHH...`, named in full in the census).
- **S71 DISARMED:** the rearm test reads FAIL because each bundle lacks four registry files, but those four are optional in the naming library and every firm's 2026-10-13 scheduled fire reads Success and wrote a record. The guard is stale, not the schedule.
- **A new fact for the packet:** 49financial's 2026-10-09 scheduled fire reads Failed in the SSM history; every later fire reads Success; the cause was not read (row D2-W378-S5). The round-191 packet reads it before any blast radius is signed.
- **Cottonwood** still serves 2026-10-08; with IB-pr-530 merged its lost account would be LISTED, not refused. The packet in round 191 counts which refused candidates publish under it.
- **Issuer defects this round:** two control slips, both in the control and not the check (the test-count floor of the fallback build; the control's first run of the rewritten test). No order amended.
- **Rows:** D2-S163 (dispositions; S71 disarmed). STILL ARMED: W374-S1 and W376-S1 (the commit-time client-data check is ABSENT on dell2; the box manager's repair), and, owner me, W349-S1, W361-S1, W348-S2, W368-S2; D2-S158 stays ARMED with the CTO. Open person-read: the export (Andrew's next export).

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
