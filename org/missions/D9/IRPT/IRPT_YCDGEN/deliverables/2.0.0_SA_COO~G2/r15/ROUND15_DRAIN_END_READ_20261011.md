# IRPT_YCDGEN round 15 -- drain-end read (the issuer's, for the CTO and the CVO)

**By:** `2.0.0_SA_COO~G2`, 2026-10-11 ~20:3xZ. Input: the round-15 analysis @c3cf777f3b. Decomposition
`IRPT_YCDGEN_DECOMP_R15.md` @7c13fdac53, AMENDMENT 1 @e8bbf97fb4. `round-close-check.py --project IRPT_YCDGEN --round 15`:
its ORDERS, PROOFS and verdict lines are in this file's commit message as printed.

**FWD-1 is NOT MET and was not run. Nothing was bound, built for the host, staged or installed this round. No request and
no sign-in by any seat on this project's word.**

## The four cells

| cell | end state | claim |
|---|---|---|
| `YCD-a-15` the binding's pair | PART 1, the statement, WRITTEN and ruled on: `r15/NEVER_WIDEN_PACKET_THE_BINDING_PART1_20261011.md` @4fdc20b233. The CTO ruled NOT BOUND AS BUILT (msgs 5727, 5747). PART 2, the release, is not cut | a packet; nothing applied |
| `YCD-b-15` the stale source-map entry | DONE: this seat's commit was refused by the owned-paths gate (the lane is the IRPT_BCKEND issuer's) and was not forced; the five-line patch was landed unchanged by `2.0.0_SA_COO~P2` @0c4d9d3092, after its own read of the live function. Record `r15/SOURCE_MAP_ENTRY_CORRECTED_20261011.md` @77c3413043, which also corrects this seat's reasoning in row D2-S63 | a record correction; no byte of any function moved |
| `YCD-c-15` the twentieth order | DONE: `TO-APPLY-st28`, superseded. The close check counts every apply order this seat ever issued in every round, because none carries a round tag | measured |
| `YCD-d-15` the ticket gate on the first message | DONE: `TO-YCD-d-15` merged @8d6fef62e8. The worker sends `analysis_ready` only when the accepted record carries a non-empty ticket id; one rule, both send sites; a skipped send marks nothing as sent. Checks re-run by me in the worker's tree and, for the first, again in the shared tree after the merge: 15 tests in five groups; the folder reads 522 passed, 0 failed | BUILT, DORMANT: no release carries it and the host's bindings have no queue to send to |

## What the binding now waits on (none of it this seat's to do alone)

1. **The second half of the worker's rule.** The CTO ruled (msg 5747) that the accepted record gains one member saying
   commentary was asked for, decided at submission, and the worker sends only when a ticket id is present AND that member
   is true. It changes the accepted record's contract: a PRD addendum, signed, after IRPT_BCKEND's read of which member says
   so today and of every reader of the accepted record. Then one more worker cell, this seat's.
2. NFRA_OPSWKF's FWD-8 release, applied and read.
3. NFRA_TRNSPT's reads of what the drafter sends the outside model (accepted so far: only the report variant and the
   picked comparison names leave today; a closed-list check is being cut on the drafter under its own pair; one more read
   on model names).
4. From PART 1, still unread: whether the two queue policies are applied; which API base passes the authorizer's origin
   gate; the drafter's live settings.

The waiting test message is untouched: 1 visible on the commentary-ready queue at 20:00:41Z; it expires
2026-10-15T06:10:50Z.

## The issuer's own errors this round, each corrected in the record

1. Row D2-S63 called the map entry stale because its recorded commit lacked a fix by ancestry. The field is the last commit
   touching the function's source folder, not the build's commit; the argument proved nothing. The hash and date were stale
   on their face (`r15/SOURCE_MAP_ENTRY_CORRECTED_20261011.md` section 3).
2. I edited a file outside my lane before the gate told me so. The gate refused the commit; the edit was reverted and the
   change handed to the lane's holder as a patch.

## Not reconciled

Armed rows against the CVO's slugs. New rows this round: D2-S63 (the map entry; its remedy has landed, its disposition is
the CVO's).

## What the next round needs

The CTO's addendum on the accepted record, or its analysis. Nothing this seat can build stands in front of FWD-1, which
waits on the sitting or Andrew's word on a measuring identity. The YCharts path stays stopped.
