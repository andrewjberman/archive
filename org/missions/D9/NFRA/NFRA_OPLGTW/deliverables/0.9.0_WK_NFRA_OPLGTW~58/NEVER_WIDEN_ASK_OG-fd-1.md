# NEVER-WIDEN ASK -- OG-fd-1 (round-35 E1): each silver sweep drains only its own family's DLQ messages

To: `1.0.0_SA_CTO~Z` and `2.0.0_SA_COO~O`. From: `0.9.0_WK_NFRA_OPLGTW~58`. Phase A (source, offline tests, this ask). No build, deploy
or SQS call has been made. Rows: `NFRA_OPLGTW-Z-W58-S1` (schwab keeps its own drain), `NFRA_OPLGTW-Z-W58-S2` (record shape unread live).

## 1. The behaviour change

Source: `data/assets/scripts/silver/mirror_conversion.py` `drain_dlq(sqs, queue_url, family, cap)`; callers `run_sweep` (same file) and
`data/assets/scripts/silver/etf_conversion.py` `run_sweep` (passes `"etf"`). New helper `dlq_message_family(body)` reads
`requestContext.functionArn` of the Lambda on-failure destination record and takes the name after `:function:` up to the next colon;
`opal-assets-silver-<family>` gives `<family>`.

BEFORE: a sweep received and deleted every message on `opal-assets-silver-dlq`, up to 100, and reported them all.
AFTER, per message:
- own family: deleted, reported in `messages`, counted in `drained`;
- another family: `change_message_visibility(VisibilityTimeout=0)`, not deleted, not reported, counted in `other_family_returned`;
- family unreadable (body not JSON, no `requestContext.functionArn`, function name not `opal-assets-silver-*`): left in the queue
  (visibility reset to 0), counted in `unattributed`, NEVER deleted.

The cap and the `truncated` flag are kept (cap counts own messages). A returned message is receivable at once, so the loop stops on a
page of only already-seen foreign messages and at 50 receive calls (`scan_truncated: true` when that bound fires). The report gains
`family`, `unattributed`, `other_family_returned`.

## 2. Both branches

1. Records carry the function ARN (the documented destination record; the queue is each Lambda's `on_failure` destination,
   `infra/aws/terraform/opal-assets/silver.tf:700`): each sweep reports and deletes only its own. Rows like Z-S91 stop.
2. Records do NOT carry it (shape differs from the document): every message reads `unattributed`, nothing is deleted, the queue keeps
   growing to its 14-day retention, and every sweep report says `unattributed: N`. No data is lost; the drain is simply idle. The live
   grade below detects this at the first sweep. Rollback is section 5.

Not covered, row `NFRA_OPLGTW-Z-W58-S1`: the schwab Lambda's own `schwab_runtime.drain_dlq` (`:247`) is outside this order's paths and still
deletes every message, including other families'. After this deploy a schwab sweep can still eat a mirror family's failure. A schwab edit
is a separate cell; the issuer decides.

## 3. Per-family PACKAGE delta the deploy would ship

Measured: each BUILD_MANIFEST `vendored_modules` file at the cut base (`91bde9b54c`) against the snapshot beside it in
`infra/aws/lambda/opal-assets/opal-assets-silver-<family>/`, as lines added / removed going snapshot to source. These are the changes a
rebuild carries IN ADDITION to this order's own change (+68 / -9 lines in `mirror_conversion.py`, +3 / -2 in `etf_conversion.py`).

| family | file | snapshot lines | source lines | beyond this change |
|---|---|---|---|---|
| orion | mirror_conversion.py | 901 | 1149 | +252 / -4 |
| orion | mirror_schemas.py | 626 | 637 | +11 / -0 |
| orion | silver_registry.py | 234 | 245 | +13 / -2 |
| eclipse | mirror_conversion.py | 805 | 1149 | +358 / -14 |
| eclipse | mirror_schemas.py | 626 | 637 | +11 / -0 |
| eclipse | silver_registry.py | 234 | 245 | +13 / -2 |
| blackdiamond | mirror_conversion.py | 1134 | 1149 | +16 / -1 |
| blackdiamond | silver_registry.py | 245 | 245 | +1 / -1 |
| blackdiamond | rebalancer_conversion.py | 613 | 670 | +67 / -10 |
| blackdiamond | rebalancer_schemas.py | 194 | 295 | +106 / -5 |
| blackdiamond | opal_strategy_matcher.py | absent from snapshot | 90 | +90 (new file in package) |
| etf | mirror_conversion.py | 1134 | 1149 | +16 / -1 |
| etf | silver_registry.py | 245 | 245 | +1 / -1 |
| schwab | (all 11 vendored files equal source) | | | 0; the change does not reach this package (S1) |
| smartx | (2 vendored files equal source) | | | 0; no DLQ read in the package |

Files not listed are byte-equal. The bd49finsurance package (silver_registry.py +1 / -1) has no DLQ reference and needs no rebuild for
this change. The etf package must ship `etf_conversion.py` and `mirror_conversion.py` together (the `drain_dlq` signature gained a required
`family`). Lambda layers are not touched.

## 4. Order of deploys

One family at a time, each followed by its live grade (section 6) before the next: 1. etf (smallest drift), 2. blackdiamond, 3. orion,
4. eclipse (largest drift, +358 / -14 in one module, deployed last so the first three have already shown the drain behaviour).
Reason: each package is self-contained and carries the same change; a failure in one family does not touch another, and the sooner a
family is changed, the sooner it stops eating foreign messages.

## 5. Rollback per family

Re-deploy the family's previous artifact (the zip it ran before, by CodeSha256 recorded in the deploy ledger entry opened at start).
The change touches no queue, role or schedule, so rollback restores the delete-everything drain and nothing else. A message left in the
queue by branch 2 stays there (14-day retention) and is read by the restored or the next working sweep. Per family: etf, blackdiamond,
orion, eclipse each roll back independently by that family's prior artifact.

## 6. The live grade the applier runs

Plant ONE synthetic family-A message shaped like a destination record on `opal-assets-silver-dlq`, with
`requestContext.functionArn` = `arn:aws:lambda:us-east-1:<account>:function:opal-assets-silver-schwab:$LATEST` and a marker in
`requestPayload`. Run family B's sweep (e.g. the freshly deployed `opal-assets-silver-orion`). Read, in B's returned/manifest `dlq` block,
that the planted marker is absent from `messages`, `other_family_returned >= 1`, and the message is still on the queue
(`get-queue-attributes` ApproximateNumberOfMessages counts it). Then run A's sweep and read that A's `dlq.messages` carries the marker and
the queue no longer holds it. Because the schwab sweep still drains everything (S1), use a mirror family as A for the second half
(e.g. plant `opal-assets-silver-eclipse` and run eclipse's sweep once eclipse is deployed), or accept that the schwab arm reads as the
old behaviour. Also read any pre-existing real messages: a sweep that reports `unattributed > 0` on real traffic means branch 2 and
stops the roll-out.
