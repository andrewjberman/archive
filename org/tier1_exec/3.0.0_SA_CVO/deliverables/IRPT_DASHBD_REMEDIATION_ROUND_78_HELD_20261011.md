# IRPT_DASHBD: rows ready to graduate, round 78 -- HELD outside the channel

Compiled by `3.0.0_SA_CVO` (seated on dell2), 2026-10-11T21:38:53Z. Input: msgs 5880 and 5882 (round 78 drained @fd9ebd2f35; orders DB-b-148 to
DB-b-150). No judgment criterion. This seat made no read of its own.

**HELD.** Three IRPT_DASHBD orders are issued (DB-b-151, DB-b-152, DB-b-153), and the corpus gate refuses a new remediation row
while an order is not terminal. OWNER: `3.0.0_SA_CVO`. UN-PARKS ON: no IRPT_DASHBD order open.

- **D2-W121-S1** (filed by `0.9.0_WK_IRPT_DASHBD~121`): DB-b-148: the producer sha256 CONTESTED_51_MEANING.json records for x1_crosstab.py does not match the tracked file's bytes; the tracked file reproduces the record's counts.
- **D2-W121-S2** (filed by `0.9.0_WK_IRPT_DASHBD~121`): DB-b-148: the three within 0.35 pp each close under BOTH START and MID, so they are among the segments where more than one timing closes, and the ruling's list of such segments (32, 11, the fee-row day) leaves them out.
- **D2-W121-S3** (filed by `0.9.0_WK_IRPT_DASHBD~121`): DB-b-148: comp-find -i with word boundaries over the repo from the worktree root did not return within the 120 s bound (rc 124); the token census was taken with native Grep.
- **D2-W122-S1** (filed by `0.9.0_WK_IRPT_DASHBD~122`): DB-b-149: on one day, 34 of the 160 per-asset medians the two price paths take over the original Black Diamond store change when each transaction id is counted once (26 under 0.1 percent, 6 between 0.1 and 1 percent, 2 over 1 percent); the Lambda path serves them, so the owner decides which weighting a price should carry.
- **D2-W122-S2** (filed by `0.9.0_WK_IRPT_DASHBD~122`): DB-b-149: infra/aws/ec2/EC2_MANIFEST.json says the bd_price_update.py script is invoked at the end of the opal-bd-allocation-download SSM sequence, but the repo's SSM document has no price step, and the live Lambda it 'replaces' is the one that ran on 2026-10-11.

**For the slug.**
- **D2-W122-S1 is the round's finding and it is about a SERVED price:** on one day 34 of 160 per-asset medians change when each
  transaction id is counted once, 2 of them by more than 1 percent. The CTO placed it (msg 5880): one more read here for the
  severity, and the row carried to the owner of the Black Diamond pipeline now. Row D2-W113-S2 stays open on it.
- D2-W122-S2: the manifest names a script step the repository's document does not have; the Lambda is what ran.
- D2-W121-S2: the three segments within 0.35 points close under both START and MID; they join the not-determined.
- D2-W121-S1 and S3 are instrument notes; to dismiss at the compile.
- The Rule 24 proposal for the timing classes waits on the CTO's ruling: two axes, six new tokens with 0 prior hits each
  (the worker's census), 47 not determined, 3 START, 1 MID.
- Not established: whether a dedupe on the id alone drops a real row among the 590 ids that repeat inside one group.
