# IRPT_DASHBD round 118 (the CTO's B-IN analysis, msg 8034), workstream B-IN (Inflection) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-15 ~04:4xZ)

**One order (a WORLD vendor read), drained; no write to AWS, nothing deployed; the raw Orion responses stay in the private folder; counts, verdict words and digests only in the repo.** Issued @251a6550f5 (merged @0057ad8e6e), amended @7fcdeb1a2c, drained: `DB-i-6` (~306, @10d7651624). On the landed tree `DBI118-1-AC1` PASSES and the proof instance reads VALID. `round-close-check --project IRPT_DASHBD --round 118` reads **MAY-CLOSE** (4 orders in round 118 across workstreams, 0 judgment criteria). Push state: LOCAL on box/dell2, not read against origin. The Scope account FEED is `~P2`'s addendum (CTO round-118 ruling 1) and is not in this packet.

## What the probe found

The same five-account household as round 117. **Four Scope calls, all HTTP 200, no retry, six seconds apart, the inner scope body:** Q3 (2026-07-01 to 2026-09-30) flag false and true, then, because the Q3 pair first read "no fee" (my rule, below), YTD (2026-01-01 to 2026-09-30) flag false and true. Credential ACCEPTED again, from Secrets Manager.

- **(i) Coverage: still short.** Q3: 4 groups for 5 accounts, 3 with a series (one account has NO group, one has a group and no series). YTD: 4 groups, all 4 with a series. **The series-less account gained a series over the longer span; the missing account did not appear in either window.** Both short accounts hold positions on 87 days of the quarter. All five accounts share one account type and registration category, so the visible pattern is not a class-based exclusion; the cause class of both stays `NOT_DETERMINED`. One account of five, that holds positions, has no Orion Scope group over two spans: that is a coverage fact the feed must carry, not one to work around.
- **(ii) The fee gap ties, on this household.** By fee magnitude, in the Q3 pair both fee-bearing accounts have a true-minus-false gap that ties to the summed fee over the start value within the pre-set tolerance (0 untied, 0 in the wrong direction); the third account has no fee and its return is equal under both flags. The verdict is `NET_WHEN_FALSE`: **`calcGrossOfFees` false is net of fees, shown on 2 fee-bearing accounts of one household in one window.** The YTD pair agrees where it can be read (1 tied, 0 untied, 2 fee-bearing accounts have a zero start value so their tie is undefined). The limits are stated: one household, two accounts, a first-order tie (fee over start value).
- **The fee sign.** The source sums fees NEGATIVE; the money is a cost.

## What this seat read for itself

I re-ran the criterion in the worker's tree (PASS), re-validated the proof instance (VALID), merged through `safe-merge.sh` (row gate clean), scanned the record, script and proof for identifier-length digit runs (none) and checked the script's token handling (it prints verdict words and counts and writes no token). **Before I amended the fee rule I computed both readings from the saved bodies** (counts only): by magnitude 2 of 2 Q3 fee-bearing accounts tie and none is untied or reversed; I did not tune the rule to reach a verdict I could not see. **Not a grade.**

## Issuer errors this round (mine, disclosed)

1. **The fee rule assumed a positive sign** (`feeAmount` above 0) with no measurement of the sign. The source sums negative, so the Q3 pair read `NO_FEE_IN_WINDOW`, the worker spent two calls on a YTD fallback the right reading would not have needed, and the row `W306-S1` went ARMED. Amended @7fcdeb1a2c: the tie uses `abs(fee)`, an account with a non-positive start value is left out of the tie, the tolerance and the direction test are unchanged, and the YTD pair stays within the four-call cap. The stale record failed the amended check and the worker recomputed it from its saved bodies, no new call.
2. The order's step 3 made the YTD fallback depend on that same sign test, so the amendment relaxed the checker's "YTD only after a feeless Q3" gate; both are disclosed in the amendment commit.

## Rows held (owners named)

`W306-S1` (BLOCKING, ARMED, owner this seat): ruled above as my error and fixed; disarm evidence is `D2-S57`. `W306-S2` (INERT): two YTD fee-bearing accounts have a zero start value, so their tie is undefined. No other ARMED row. The commit gate's account-id check did not run (`W182-S1`'s condition, owner `0.0.0_AB_MSTR`).

## What goes to the CTO

1. **Fee basis:** the CTO's ruling 3 said "if (ii) ties, `fee_basis` becomes NET and the page states it". It ties on one household's two fee-bearing accounts. The feed's `fee_basis` can read NET with a stated scope ("shown on a sample, one household"), or stay `UNPROVEN` until a second household ties; I recommend recording NET with the sample size in the feed's `fee_basis` note, since false is the request the estate already sends and the page prints the basis it can show.
2. **Coverage:** the missing account is persistent, not a window effect. The feed's `ABSENT` row with `NO_GROUP` (never a zero, never an Opal fill) is the right treatment; the cause (why Orion's Scope omits an account that holds positions) is not read and cannot be read from the repo. Whether to ask Orion is a vendor-contact matter and Andrew's, not this lane's.
3. **This lane has no further cell** unless the CTO names one. The remaining B-IN work is `~P2`'s feed, then B-IN's adapter reading it (the account returns switch from `NO_SOURCE_YET` to Orion's figure with `source: orion`). I would cut the adapter cell in the round after the feed lands its first bronze and silver; until then it has nothing to read.

## What this does to the FWD outcomes

Inputs to `FWD-2` for Inflection: not met. The account pages stay "Account-level returns are not available for this firm yet." until the feed lands and the adapter reads it.

## Open

**Andrew:** nothing from this workstream. **This seat:** the next B-IN cut waits on the CTO's round-119 B-IN analysis or on `~P2`'s feed landing.

-- 2.0.0_SA_COO~I2
