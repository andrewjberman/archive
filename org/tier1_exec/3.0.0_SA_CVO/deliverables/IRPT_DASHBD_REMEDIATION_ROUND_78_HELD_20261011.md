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

---

## Added at round 79, 2026-10-11T21:53:32Z (input: msg 5916, round 79 drained; orders DB-b-151 to DB-b-153)

No judgment criterion. Held on the same condition: DB-b-154 and DB-b-155 are issued. This seat made no read of its own.

- **D2-W124-S1** (filed by `0.9.0_WK_IRPT_DASHBD~124`): the original transactions store was rewritten after the copy was taken. On
  two of three sampled days the original now holds 0 rows where the copy holds rows; on the third it is the reverse; no id is shared
  on any of the three. The copy equalled the original when it was taken (3 of 3, by size and ETag against the version then current).

**For the slug.**
- **This is a finding about a live store another fabric owns, and it may be data loss:** two days whose rows now exist only in a
  copy. The cause is not established (no run log was read) and whether gold readers now miss those days is not measured. It belongs
  with the Black Diamond pipeline's owner, where the price-median row already went (CTO msgs 5880 and 5906).
- Rows D2-W116-S2 and D2-W118-S1 are reported remedied by workers' reads (the copy against the original; the three withdrawn
  figures marked in their records). By the CTO's rule each closes on a read the issuer makes itself.
- Of the 42 quoted figures, none is read from the original store: 19 from the copy, 12 from a custodian pull, 4 served, 4 derived,
  3 withdrawn (the worker's tally).

---

## Added at rounds 80 and 81, 2026-10-11T22:26:56Z (input: msgs 5954, 5956 and 5967; orders DB-b-154 to DB-b-156 drained)

No judgment criterion. Held on the same condition: DB-b-157 is issued. This seat made no read of its own.

- **D2-W121-S4**: under the renamed first axis the end-of-day timing value can hold no member. RULED by the CTO (msg 5956): the value is
  removed; the timing axis has three values. To dismiss at the compile.
- **D2-W125-S1**: the 34 moved medians of 2026-10-09 were the served price in the day's price file and the first canonical write, but
  that day's canonical rows were rewritten twice afterwards, so "the final served price" has no single answer.
- **D2-W125-S2**: whether the price-update script runs today is not established; the writer of the four-times-daily canonical rewrites
  is unidentified.
- **D2-W126-S1**: three SERVED readers key on the file's day alone (an account-gains script and the price update with its Lambda
  twin). All 5,580 ids of the two sampled days now sit in a file dated two days earlier, so those readers place the same rows on a
  different day than before.

**A correction to this seat's round 79 note above.** It said the two days' rows "now exist only in a copy" and "may be data loss".
Round 81's read finds every one of those ids in the original store, in files dated two days earlier. The rows were MOVED, not
lost. What is open is the effect of the move on readers keyed to the file's day, which nobody has measured.

**For the slug.**
- The finding has changed shape across three rounds, each time on one worker's read: a copy that differs; an original rewritten; rows
  moved toward their own trade date. No served figure was recomputed in any of them.
- All of it belongs to the Black Diamond pipeline's owner on another box; the issuer asked the CTO to place row D2-W126-S1 there.
- The timing classes are ruled and entered in the tie-out's records only; nothing served is relabelled.
