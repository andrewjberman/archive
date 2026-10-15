# IRPT_DASHBD round 120, workstream B-IN (Inflection) (the CTO's B-IN analysis, msg 8081) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-15 ~05:4xZ)

**One order (a WORLD vendor read), drained; TWO Scope calls; no write to AWS, nothing deployed; the raw responses and the roster stay in the private folder; counts, verdict words and digests only in the repo.** Issued @5d4d069ce1 (merged @e9a946b067). Drained: `DB-i-8` (~308, @1e83135577). On the landed tree `DBI120-1-AC1` PASSES and the proof instance reads VALID. `round-close-check --project IRPT_DASHBD --round 120 --workstream B-IN` reads **MAY-CLOSE** (1 order, 0 judgment criteria). Push state: LOCAL on box/dell2, not read against origin.

## What the probe found

The household was chosen by the rule fixed before the call (11 candidate households other than round 117's, none with an account outside the active roster; the lowest digest): **six accounts, four FULL, one NO_START, one NO_MODEL.** Two Scope calls, inner body, `calcGrossOfFees` false: Q3 and YTD, both HTTP 200, six seconds apart, no retry. Credential ACCEPTED (a fifth time).

Per window (Q3 and YTD alike): **5 accounts `GROUP_WITH_SERIES`, 1 `NO_GROUP`.** The prediction written in the order before the call, part by part:

| part of the prediction | held? |
|---|---|
| the NO_START account (null `accountStartDate`) has NO Scope group in both windows | **HELD** (`NO_GROUP` in Q3 and in YTD) |
| every OTHER account is `GROUP_WITH_SERIES` in both windows | **HELD** (4 of 4 in each window; 0 short cells) |
| the NO_MODEL account (a start date, no `modelName`) is not `GROUP_WITH_SERIES` in Q3 | **DID NOT HOLD** (it has a group with a series in Q3 and in YTD) |

**Reading, two households now.**
- **A null start date at the source goes with NO Scope group: 2 accounts of 2 (one in each household), both windows.** This is the class that explains the account Scope omits, and it is now a measured pattern on two households, not a one-account inference. Firm-wide the roster holds 40 such accounts among the dimension's 863 that are in it. A household-level reading still rests on two households; the claim says so.
- **A missing model does NOT go with a short Scope result.** Round 119's series-less account had no model; this round's no-model account is complete in both windows. So the round-119 inference "no `modelName` explains the group with no series over Q3" is **refuted as a general rule** by a counterexample. What made round 118's account short in Q3 and complete over YTD is not explained by anything this lane has read.
- The CTO's all-or-nothing rule (ruling 2) therefore reads `claim_upgrade_allowed: false`. Read on its two parts, the evidence supports upgrading ONE reason class and not the other (below).

## What this seat read for itself

I re-ran the criterion in the worker's tree (PASS), re-validated the proof instance (VALID), merged through `safe-merge.sh` (row gate clean), scanned the record, script and proof for identifier-length digit runs (none), and checked the per-window state counts and the verdict fields in the record against the order's prediction. **Not a grade.**

## Issuer errors this round

None found.

## Rows held (owners named)

`W308-S1` (ARMED, owner this seat): the commit gate's account-id check did not run on dell2, the same condition as `W182-S1` (owner `0.0.0_AB_MSTR`, infrastructure); `D2-S63` records this seat's identifier scan as the stand-in and carries it INERT. `D2-S60` (the CTO's ARMED row, my disarm) stays half met: the read half is in `D2-S61`; `~P2`'s feed half has not landed. No ARMED row has a dark owner.

## What goes to the CTO

1. **Reason classes for `~P2`'s feed.** `NO_START_DATE_AT_SOURCE` can carry `claim: measured (2 households, 2 accounts)`. **`NO_MODEL_AT_SOURCE` should NOT be used:** a counterexample contradicts it. An account with a group and a series never needs a reason; an account with a group and no series stays `GROUP_NO_SERIES` with the reason `NOT_DETERMINED`. The page words may follow the measured class ("Orion has no start date recorded for this account") and stay neutral for the rest.
2. **The source fix** (Inflection's operations setting the start date on the 40 accounts) now has its measured pattern and is the CTO's act for Andrew with a draft. The draft names the count (40) and the one field (`accountStartDate`, with `accountStartValue` null alongside it), not the model.
3. **This lane has no further cell** unless the CTO names one. What remains for B-IN is the adapter cell, after `~P2`'s feed lands its first bronze and silver.

## What this does to the FWD outcomes

Inputs to `FWD-2` for Inflection: not met. The account pages stay "Account-level returns are not available for this firm yet." until the feed lands and the adapter reads it.

## Open

**Andrew:** the source-fix draft (the CTO files it). **This seat:** the adapter cell waits on `~P2`'s feed; the next B-IN cut waits on the CTO's round-121 B-IN analysis or on that landing.

-- 2.0.0_SA_COO~I2
