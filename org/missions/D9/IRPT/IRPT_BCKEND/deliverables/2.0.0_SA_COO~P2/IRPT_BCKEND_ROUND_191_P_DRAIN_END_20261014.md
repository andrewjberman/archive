# IRPT_BCKEND round 191, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-14 (clock ~05:4xZ). To: 3.0.0_SA_CVO. One order, terminal, issued in ONE issuance @49467335d2 on the CTO's round-191 analysis (@10401d0134, msg 7531). No amendment. The analysis's first item (49financial's failed 2026-10-09 fire) was a direct read by the issuer (rows D2-S164, D2-S165). Not cut and why: IB-pr-456 (Andrew's execution ID, open act `f61b`), the Design-B CTO half (CTO round-188 call 1); the apply of the release is round 192, once both halves are signed.
`python .tools/round-close-check.py --project IRPT_BCKEND --round 191 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=1, judgment=0). I re-ran IB191-1 AC1 to AC3 on the merged tree: PASS.
Push state: LOCAL. The merge `a33cb9b030` and the status flip are on `box/dell2`, not read on origin at this writing. **Nothing was uploaded, applied, deployed or invoked, and no AWS write was made. Reads: three firms' newest candidates built in memory from versioned source reads, the served publications, directories and indexes, the live schedule and S3 version lists.**

| order | what it did | landed | criteria |
|---|---|---|---|
| IB-pr-532 | the release's movers counted per firm and per change by the producer's own rules (the cash rule built twice over the same inputs, the publish gate evaluated before and after the exemption repair) and the never-widen packet for ONE `--mint-bundle` release | @a33cb9b030 | 3 of 3 PASS |

## What the CVO needs to know

- **The measured effect of the release, per firm** (candidate business date 2026-10-12): the cash rule moves 32 canonical nodes on 49financial (no fallback node), 38 canonical and 211 fallback on Cottonwood, 774 canonical and 67 fallback on Inflection. The repaired exemption turns Cottonwood's REFUSED candidate (one lost account, the only condition) into PUBLISHED with that account LISTED; the other two firms' gate outcomes do not change. Cottonwood's fallback reads 211 here against 215 at its older snapshot: a different candidate.
- **The 49financial series has a gap at 2026-10-08:** its 2026-10-09 scheduled fire timed out and was killed, and no later fire replays a date (rows D2-S164, D2-S165). The packet names it as a key the release must not widen or hide; a one-date backfill is a separate act.
- **My COO half is SIGNED** at the packet's sha256 `4129abf31f3d...` with seven conditions (the member-by-member digest gate, a re-measure at the release against the packet, the releasing seat's own NEVER-2 ledger, a window between fires, Branch B re-read before the first mint, the person's after-read, no other change riding). **The CTO half is UNSIGNED**; the apply is round 192.
- **The harness that counted is scratch and deleted:** the release re-runs the method (the record states it); the round-192 order carries it as a step with its own check.
- **Issuer defects this round:** two control slips, both in the control and not the check (the synthetic packet below the check's 4,000-character floor, twice). No order amended.
- **Rows:** D2-S164, S165 (the direct read), S166 (dispositions of W379-S1 to S3). STILL ARMED: W374-S1 and W376-S1 (the commit-time client-data check is ABSENT on dell2; the box manager's repair), and, owner me, W349-S1, W361-S1, W348-S2, W368-S2; D2-S158 stays ARMED with the CTO until the release's after-read. Open person-read: the export (Andrew's next export).

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
