# IRPT_BCKEND round 168, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-12 (the clock read 22:47Z when this was written). To: 3.0.0_SA_CVO. ONE order, terminal, issued on the CTO's ROUND-168 ANALYSIS section 3 item 1 (msg 6559) and amended twice (below).
`python .tools/round-close-check.py --project IRPT_BCKEND --round 168 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=1, judgment=0, proofs 1 of 1 OK). The issuer re-ran IB168-1-AC1, AC2 and AC3 itself after the executor's report: all three PASS (AC2 is a live AWS read at the check).
Push state: on origin @0fe66cb805 (ls-remote read 22:47Z, equal to this tree's HEAD).

## What landed (a WORLD act)

`IRPT_BCKEND.TO-IB-pr-487`, `0.7.0_AE_CloudOps~IB2`, record `deliverables/0.7.0_AE_CloudOps~IB2/IB168-1_release_after_reads.json`, commits 761f2559fe and 30b34d521d.
`irpt-performance-adapter` moved from `kMB8xCI93/9QLUnzglVIs0EIRY07SSLBiU5ln8iJwUc=` to `abep4h7RngMS9JomQUdkcOT3EZ+W953OdxeK0HkdzFo=` at 22:35:06Z (the issuer read the live CodeSha256 at 22:35Z and again in AC2). One member changed, `holdings_gold.py` (1 of 71): the claim on a figure chained over a day that left a return out now follows that day's status, and two counts appear beside `days_linked`. No figure moves (30,843 of 30,843 equal, the round-167 worker's offline read).
Path: ledger `-r3` opened and closed, source-map re-pin `3381c42f13` (touched only the map), BUILD_ONLY digest matched, rollback S3 version `F.G7ZDSN...` named before the upload (64 versions listed), planfile 1 change 0 destroy through `safe-apply`, re-plan 0, 0 `TypeError` lines (the issuer read the log group from 22:35:06Z: 0 TypeError events; the only 9 function log lines since the apply are the executor's own smoke invokes).

## THE SERVED CHANGE IS NARROWER THAN THE PAIR WAS SIGNED ON (issuer error, corrected)

The round-167 packet, my COO half and the CTO half all quoted two MOVES rows: 49F (SI 23, YTD 19, QTD 2, 1Y 20) and orion (SI 750, YTD 76, QTD 7, 1Y 106). IB2 found that the deployed function answers performance only for a firm in `COMPOSED_FIRMS` with a holdings source, which today is Inflection (orion) alone: 49 Financial is refused by design (`retained.py:175`, P-6) and Cottonwood has no holdings source. I read `retained.py:171-195` at HEAD. **The 49F row is struck; the served change is orion only** (CTO half AMENDMENT 2 @4936559bbd, COO half AMENDMENT 2 signed 22:14Z). Not established: whether another function serves 49 Financial through the same reader.

## What was NOT exercised live (stated, not hedged)

- **The changed Inflection path has not run on a live answer.** The after-read of CTO AMENDMENT 1 (read kept selections before and after, claim equal to the predicted claim) needed a selection record the executor cannot read or write and no grant was added (row S112). The nine selections `2.0.0_SA_COO~D2` kept from its UI walks are eight 49financial and one cottonwood; all nine refuse before any compute, so they are the IMPORT SMOKE only: the same refusal code before and after (8 `PathARetiredForFirm`, 1 `VendorEgressRefused`). `2.0.0_SA_COO~D2` could not reach an Inflection client (the walker cannot set the header Firm control; the page ignores `?firm=` for an internal viewer). The CTO named fallback (B): arms 1 to 4 are graded `UNEXERCISED-LIVE` on the packet's offline replay (30,843 equal); persisted retained revisions: 0.
- Claim class of the evidence: the live digest, the plan, the log and the smoke are MEASURED; the claim behaviour of the changed rule on the served gold is the worker's OFFLINE replay (measured by a worker, not by this seat), not an answer the deployed function gave.
- Per the record's `not_established`: the nine before-invokes ran under the preceding stop (ledger -r2, 22:04Z to 22:07Z) with live unchanged, not re-run after the re-cut; per-ref classes were mapped to refs by invoke order against the function log; the per-ref firm and window came from a file D2 INFERRED from page and log order.

## Open item with an owner and the condition that closes it

**Owner `2.0.0_SA_COO~P2`; condition: the first organic Inflection answer after 22:35:06Z.** Instrument: the function's `irpt_retained_phases` log lines (`path` other than `refused:*`) and the answer's claim and counts; 0 TypeError. None has appeared (9 lines since the apply, all the smoke). Branch B (redeploy the named rollback version through the same Terraform path) stays available. This is a wait, stated as one: no act a seat can take on demand exercises the path (no Inflection selection can be obtained; the only fix is a walker flag that selects the header Firm option, a change to the shared `/ui-walk` skill, not mine to make).

## Rows

- `IRPT_BCKEND-D2-S112` (BLOCKING, INERT; IB2): the arms needed a selection record. Resolved by the CTO's AMENDMENT 1 and the cut; the order then ran.
- `IRPT_BCKEND-D2-S113` (BLOCKING, INERT; IB2): 0 of 9 refs read through the function. Resolved by AMENDMENT 2 (orion-only served change, fallback B). The unexercised path is carried above, not in the row.
- ARMED rows opened or left in this round: none.

## Issuer defects this round

- The arms and AC3 were written (round 168 cut) on selection-keyed invokes without reading how a selection is created or which firms the function serves; two stops (S112, S113) and two order re-cuts (AMENDMENT 1 and 2) followed. AC3 was rewritten twice, each time with a good record and tampered controls; AC1 and AC2 were not changed. No gate limb graded the amendments except GATE (viii), which found none.
- The MOVES table in the COO half's section 1 still reads the struck 49F row; AMENDMENT 2 says so beside it.
- The write ceiling was raised from 8 invokes to 18 and named in both halves (CTO accepted, msg 6616); it was not used (0 persisted).

## Judgment criteria

None.

## Request

L8 compile and L10 stamp for round 168. MAY-CLOSE is read on the strength of an applied, digest-verified, log-clean release with its changed path unexercised live; if the compile reads that as not closable, the organic read above is the one act that would change it.

Carried to the next round (the CTO's list, not decided here): the `bd_adapter.py` rename's own build and pair (its APPLY waits on Andrew's PROD promote of the portal reader, `dell1-e7f2`); the DSGN_IRPTV1 row W63-S1 fixture cell (CTO msg 6626); no new cell is cut mid-round.
