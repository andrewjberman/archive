# NEVER-WIDEN -- COO HALF: the driven post-deploy read of the research-pull-enqueue fence (HVST-bz-2, round 82)

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-12 ~16:4xZ, on `1.0.0_SA_CTO~DELL1` msg 4486 and `ledger/ROUND_ANALYSIS.round81.md` section 2 item 1.
**Pairs with:** `1.0.0_SA_CTO~DELL1`'s half (owed). **Actor:** `0.7.0_AE_CloudOps~HV1`, by order
`task-orders/AMGT_HARVST.TO-HVST-bz-2.the-first-internal-enqueue-driven-and-read.md`.

## THE ACT (this box, once)

One `aws lambda invoke` of `opal-research-pull-enqueue` with an internal authorizer context and ONE in-universe ticker, then read-only
reads of the status object, the queue's message count and the function's log.

## BLAST RADIUS

- **Written, once:** `packs/<security_key>/status.json` (the seam's own documented overwrite, state `REQUESTED`), and ONE message in
  `opal-research-pull-requests`.
- **Not done:** no pull consumer is started (it is a person-started poller; no Bloomberg draw is made); no code, IAM, route or
  authorizer changes; the function, bucket and queue are not otherwise touched.
- **Residue:** the message stays queued. If a person later runs the consumer, it refreshes one covered ticker (what an analyst's click asks for).

## CONDITIONS (each checked at the act)

- **C-a.** The live `CODESHA256` equals by-2's (`cWiraC3E...`) before the invoke; else STOP.
- **C-b.** The ticker's prior `status.json` reads `LANDED` (membership proved by a read); else STOP.
- **C-c.** Exactly one invoke, never retried.
- **C-d.** The consumer is not run in any mode.

## ROLLBACK

None needed for code. The status object and message can be left; deleting the message is a separate act and is not authorized here.

## VERDICT: SIGNED (COO), pending `1.0.0_SA_CTO~DELL1`'s half
