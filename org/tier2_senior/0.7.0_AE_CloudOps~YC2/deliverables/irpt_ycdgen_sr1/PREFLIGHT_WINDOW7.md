# IRPT_YCDGEN.TO-APPLY-sr2 -- WINDOW 7 PREFLIGHT (0.7.0_AE_CloudOps~YC2)

Order: `org/tier2_senior/0.7.0_AE_CloudOps~YC2/task_orders/IRPT_YCDGEN.TO-APPLY-sr2.served-read-window-7-status-reread-dell2.md`,
issued @0d42c732d3. Issuer msg 4158 read and acked. `<risk>WORLD</risk>`, `<proof_genre>DEPLOY</proof_genre>`.
Window 6's act again for ONE more read, ruled by `1.0.0_SA_CTO~DELL2` msg 4152 (a re-read of REQ-5e4149d2's
status-job with the portal's date opt-in header).

STATE: HOLDING. Not begun. The START CONDITION is the issuer's GO naming THIS order, sent when the
window-7 laptop secret ADD is put.

## GO -- RE-MEASURED, not carried over from window 6

A half binds to the BYTES it signed, so a second window under the same half is not covered by the first
window's verification: the packet could have been amended for window 7 in between, which would leave the
half bound to bytes that no longer exist at HEAD. Both ends were therefore re-read:

- Packet `...r7/NEVER_WIDEN_PACKET_SERVED_READ_WINDOW.md`:
  - `git rev-parse HEAD:<packet>` -> `716925a28e88cf24e5ba7206edc5bc6e920fe471`
  - `git hash-object <packet>` (working tree) -> `716925a28e88cf24e5ba7206edc5bc6e920fe471`
  - negative control, a sibling packet in the same directory -> `e8aa773790...`, so the read discriminates.
- CTO half `...1.0.0_SA_CTO~DELL2/NEVER_WIDEN_SERVED_READ_WINDOW_CTO_HALF.md`: last commit `da885deef2`,
  unmoved since window 6, **Verdict GIVEN** against blob `716925a28e`.

VERDICT: the packet is byte-identical to what the CTO signed, and the half has not moved. The half signs
FIVE LEGS under conditions 1 to 5 and names no window number; window 7 is those same five legs with the
same blast radius (ONE `opal-users-v2` item), so it is inside the signed act rather than an extension of it.
Condition 4 admits an MSTR-seated CloudOps lane as substitute operator, which is this lane.

## Before-read (CTO half condition 1) -- MEASURED, read-only

`aws dynamodb get-item --table-name opal-users-v2 --consistent-read` on
`PK=USER#svc-irpt-analysis@opalinvest.com / SK=PROFILE`:

    allowedFirmIds: cottonwood
    status:         active
    userType:       service
    updatedAt:      2026-10-11T04:53:41.258001Z

claim: measured. W1's `ConditionExpression` (`allowedFirmIds = cottonwood AND userType = service AND
status = active`) will fire. No STOP condition at preflight.

CONTINUITY STATED ON `allowedFirmIds`, PER THE ORDER AND ROW `IRPT_YCDGEN-D2-S25`: the property the bounds
name reads `cottonwood`, which is the state window 6's W2 left and the state W1 requires. The `updatedAt`
value happens to equal window 6's own W2 write, which would mean no `/auth/login` has landed since -- but
that is NOT offered as a no-third-party claim, because `/auth/login` also writes `updatedAt` and its absence
from the stamp proves only that no login happened to land, never that nothing else could have.

## Preflight limbs

- `comp-schedule`: DECLARED-NOT-APPLICABLE per the order -- two conditional row writes; no schedule, trigger
  or rule.
- `comp-iam`: DECLARED-NOT-APPLICABLE per the order -- no IAM change on dell2; the secret resource-policy
  ADD/REMOVE is the laptop executor's leg, routed by MSTR. This lane performs no secret read and no IAM act.
- `comp-adversary`: RUN on the packet (re-run for this window rather than cited from window 6, since source 4
  is comp-state drift and does move). Same single flag, a PARSER zero: 3 commit-shaped hex runs present
  (`20261009`, `5e4149d2`, `5e4149d2863aea31cc87d660`) with 0 parsed as pins -- a date and the request id,
  not pins. The one pin that gates the act was verified above by printing bytes with a negative control,
  never by the parser. No open item.

## Window state read

- Window 6 closed: ledger `irpt-ycdgen-served-read-w6` CLOSED 20261011T045706Z, all 5 legs proven, order
  flipped to complete @001b7c3a34.
- `org/critical_paths/.open_deploys/` holds no `irpt-ycdgen-served-read-w7` entry (listed with `ls -a`, since
  `ls -1` hides `.unindexed_red_state.json`). Denominator is THIS tree only -- a worker tree would hold its
  own, and no worker is live on this order.
- Script unchanged: `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st29_release/swap_svc_firm.py`
  -- ONE conditional `UpdateItem`, prints `before:`/`after:`, never the password hash, ASCII only.

## On GO, in order

1. Open ledger `irpt-ycdgen-served-read-w7` (legs W1 S+ R W2 S-) and commit it.
2. `python swap_svc_firm.py cottonwood 49financial` -> `W1_SWAP_OUT_WINDOW7.txt`; record T0 from the clock
   AFTER the write returns; tell `2.0.0_SA_COO~G2` that W1 is closed, with T0 and the bound.
3. At the issuer's "R done" or T0 + 30 minutes, whichever is first:
   `python swap_svc_firm.py 49financial cottonwood` -> `W2_SWAP_BACK_WINDOW7.txt`.
4. After-read: svc reads `cottonwood`, confirmed OFF-INSTRUMENT by a separate ConsistentRead get-item with an
   absent-key negative control and the type tag shape-checked against the st28 `.L`-reads-`[]` trap. Close the
   ledger once S- is confirmed by MSTR. If the after-read is not as expected: STOP, restore, report to
   `1.0.0_SA_CTO~DELL2`.

Hard bound: W2 runs within 30 minutes of W1 in EVERY branch -- R done, R failed, or no R.
