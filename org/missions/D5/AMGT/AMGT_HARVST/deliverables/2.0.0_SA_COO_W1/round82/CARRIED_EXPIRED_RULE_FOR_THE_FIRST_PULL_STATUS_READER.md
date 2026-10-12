# CARRIED -- the EXPIRED rule for a research pull status, owed to the FIRST cell that reads pull status

**Carrier written by:** `2.0.0_SA_COO~W1`, 2026-10-12 ~17:0xZ, on `1.0.0_SA_CTO~DELL1` msg 4505 and `ledger/ROUND_ANALYSIS.round82.md` ADDENDUM 1
("neither A nor B -- YAGNI; the rule rides the first reader cell"). **Owner of the carry:** the COO of the project whose cell first reads
pull status (today `2.0.0_SA_COO~R1`, AMGT_RESAPP). **Un-parks on:** a cell is cut that reads `packs/<security_key>/status.json` for display
or decision.

## THE FINDING (state coherence, Rule 24 iv; CTO `ROUND_ANALYSIS.round82.md` section 2)

The research pull queue `opal-research-pull-requests` keeps a message for **1 day**, and the pull consumer runs only when a person starts
it (`pull_consumer.py`: "NEVER a persistent service"). An enqueue not drained within a day leaves `packs/<key>/status.json` reading
`REQUESTED` with nothing behind it: a status that names a state the system can no longer reach. Specimen: SAP GY Equity, enqueued
2026-10-12T16:43:38Z (status VersionId `F8iBxqlr2MQsG3iRuhj4JUr74oPZcs3w`, `requested_at` 16:43:40Z), expires about 16:43Z 2026-10-13.

## THE RULE (no new writer, no sweeper, no alarm: the standing moratorium)

**A reader computes the state at READ TIME.** A status whose `state` is `REQUESTED` and whose `requested_at` is older than the queue's
retention (1 day) is reported as `EXPIRED`. Nothing is written back.

## THE THREE ARMS (the criterion the first reader cell carries)

1. a `REQUESTED` status younger than the retention reads `REQUESTED`;
2. a `REQUESTED` status older than the retention reads `EXPIRED`;
3. a `LANDED` status is unchanged (and so is `FETCHING` and `FAILED`).

SAP's object is the live specimen after 16:43Z 2026-10-13, or a planted copy today.

## WHY IT IS NOT A CELL OF AMGT_HARVST (measured 2026-10-12 ~16:55Z)

No reader exists as code. Denominator searched: `lib/research`, `portal/src`, `infra/aws/lambda`, `integrations/bloomberg/research`. The only
code touching the key is the enqueue Lambda (writer), `pull_consumer.py` (writer; reads the object only to merge `requested_at`) and tests.
`scoped_amgt.py` has no pull-status read. A function with no caller is premature (the CTO's YAGNI ruling). Note the correction to the ruling's
wording: `AMGT_RESAPP.TO-AMGT-rk-7` (round 12) is `complete`, not staged, so it is not the carrier; the carrier is whichever cell is cut next.
