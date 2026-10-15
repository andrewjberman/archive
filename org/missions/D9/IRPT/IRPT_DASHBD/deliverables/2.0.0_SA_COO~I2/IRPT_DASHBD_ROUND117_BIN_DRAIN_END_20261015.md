# IRPT_DASHBD round 117 (the CTO's B-IN analysis, msg 7985), workstream B-IN (Inflection) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-15 ~04:0xZ)

**One order (a WORLD vendor read), drained; no write to AWS, nothing deployed; the raw Orion responses stay in the private folder; counts, verdict words and shapes only in the repo.** Issued @dee18705c0 (merged @f240990cfd), amended @1009b791fa, drained: `DB-i-5` (~305, @95e5d39a1e). On the landed tree `DBI117-1-AC1` PASSES and the proof instance reads VALID. `round-close-check --project IRPT_DASHBD --round 117` reads **MAY-CLOSE** (1 order, 0 judgment criteria). Push state: LOCAL on box/dell2, not read against origin.

## What the probe found

The household is the lowest-hash one with 2 or more accounts (a rule the checker recomputes): **5 accounts**. Window 2026-10-01 to 2026-10-13. **4 Scope calls were made, the whole cap:** the first two (flag false, then true) drew HTTP 400 because of my order (below); the last two, with the corrected body, drew **HTTP 200 and 200**. Six seconds apart, no retry.

- **(c) The credential is ACCEPTED** (measured: a 200 on `POST /api/v1/Reporting/Scope` with the estate's session token, loaded once per run from Secrets Manager `orion/jwt/current`; no 401 or 403 at any point).
- **(a) Multi-account: FEWER_GROUPS, not the full answer.** The vendor DID return Account groups for a five-account household in one call, so **the one-account limit is the code's** (`orion_account_mapping.py` refuses a multi-account household), not Orion's. But it returned **4 Account groups for 5 accounts, and only 3 of the 4 carry a return and a daily series.** I checked the shortfall against the position cache (flags only): **all 5 accounts hold positions on all 13 window days**, so neither shortfall is an account that was closed or not yet open. One account has no group at all; one (the oldest, 2,328 position days) has a group with no return and no series. The cause is not read.
- **(b) The fee flag is honoured; its basis is not proven.** The rule's output is `DIFFERENT_UNTIED`, which here means "the flag changes the number but nothing ties". Across the 3 accounts with a return in both responses, **the return with `calcGrossOfFees` true is higher than with false on 3 of 3 (0 equal, 0 lower)**, the direction expected if false is net of fees. The tie to `feeAmount` cannot be made: the `feeAmount` field is on 39 breakdown points of the response and **sums to zero on every group in this window**, so no fee exists to tie the gap to. A window that holds a fee date is needed (I did not assume the fee dates).

## What this seat read for itself

I re-ran the criterion in the worker's tree (PASS), re-validated the proof instance (VALID), merged through `safe-merge.sh` (the first attempt lost the race to other seats' commits three times and landed nothing; the retry landed clean), scanned the record and script for identifier-length digit runs (none) and read the script's token handling (it prints verdict words and counts, sets the token to none after the calls, and writes no token anywhere). I opened the two private response bodies myself for group counts, the sign of the true-minus-false difference and the `feeAmount` carriers; I printed no value. **Not a grade.**

## Issuer errors this round (mine, disclosed)

1. **The order never said which part of `requests_for`'s result to POST.** It returns `{"scope": scope}` and the estate posts the inner `scope`; the worker posted the wrapper and drew two 400s, which spent half the call cap. Amended @1009b791fa (AMENDMENT 1: post the inner scope; two calls left; the record lists all four calls); the order was reopened and the same worker re-ran.
2. **My check read a 400 as a credential refusal** (`REFUSED`). Amended in the same commit: `REFUSED` only when every call is 401 or 403, a new `REQUEST_REJECTED` for a rejected body, and the stale record failed the amended check as it should.
3. A clock slip in earlier notes: I wrote "~03:55Z" in the round-115 and round-116 packets while `date -u` read about 03:2xZ. The commit times are the record.

## Rows held (owners named)

`W305-S1` (BLOCKING, ARMED, owner this seat): ruled above as my error and fixed; disarm evidence is `D2-S54` (the amended order, the rerun PASS and the 2xx). No other ARMED row. The commit gate's account-id check did not run on these commits either: `W182-S1`'s condition, owner `0.0.0_AB_MSTR`.

## What goes to the CTO

The ruling's rule 3 was "if (a) and (c) pass, `~P2` adds the feed". (c) passes. (a) passes in kind (Scope returns per-account groups for a multi-account household) and fails in coverage on this household (3 of 5 accounts carry a series). I would not cut `~P2`'s feed on this alone. Two choices, both the CTO's:

1. **One more paced probe (2 to 4 calls, same household):** a window that holds a fee date and covers a longer span (for example the quarter that ended 2026-09-30), to see whether the missing account and the series-less group appear and to tie the fee gap. It would settle (a)'s shortfall and (b)'s basis together. It needs a new order and a new cap.
2. **Cut the `~P2` feed now** with a coverage rule in the feed itself (an account with no series prints "not available", never a figure), and let the fee basis print as "not stated by the source" until a fee-date window ties it.

My recommendation is 1: the two shortfalls and the fee basis are the three facts the page would state to a client.

## What this does to the FWD outcomes

Inputs to `FWD-2` for Inflection: not met. The account pages stay "Account-level returns are not available for this firm yet." until a sourced account figure lands.

## Open

**Andrew:** nothing from this workstream. **This seat:** the next B-IN cut waits on the CTO's round-118 B-IN analysis.

-- 2.0.0_SA_COO~I2
