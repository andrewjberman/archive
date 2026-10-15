# IRPT_DASHBD round 122, workstream B-IN (Inflection) (the CTO's round-118 ADDENDUM 2, msg 8455) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-15 ~17:2xZ)

**One order (a WORLD vendor read), drained; TWO Scope calls; no write to AWS, nothing deployed; the raw responses stay in the private folder; counts, verdict words, digests and timings only in the repo, and no date.** Issued @ba63063b03 (merged @a2f748c5f2), amended @8146c5c082, drained: `DB-i-9` (~309, @9da00aff3f). On the landed tree `DBI122-1-AC1` PASSES and the proof instance reads VALID. `round-close-check --project IRPT_DASHBD --round 122 --workstream B-IN` reads **MAY-CLOSE** (1 order, 0 judgment criteria). Push state: LOCAL on box/dell2, not read against origin. This round is cut on the round-118 addendum, not on a new CTO analysis.

## The bound for pair (b) ADDENDUM 2 (what `~P2` is waiting for)

Two households called, one Scope call each, from the household's earliest Orion account start date to 2026-10-13, Daily, inner body, `calcGrossOfFees` false, both HTTP 200, no retry:

| | call time | response size | accounts | with a series |
|---|---|---|---|---|
| household A (5 accounts) | 1.68 s | 416,350 bytes (0.42 MB) | 5 | 4 |
| household B (6 accounts) | 1.83 s | 1,145,365 bytes (1.15 MB) | 6 | 5 |

**For the whole universe: 294 requests** (one per household of the dimension that has at least one account in Orion's active roster), **a serial upper bound of about 537 s (9 minutes)** (294 times the slowest call) **and about 337 MB** (294 times the largest response). The 180 s timeout was never approached (the slowest call used about 1 percent of it). What the bound is not: no parallelism assumed, no retry, and the rate-limit headroom was not measured (two calls cannot show it); the feed's own limiter paces the real run. The household B call is the larger because its oldest account has a 2,228-day series; the 337 MB is therefore a conservative ceiling (the average response should sit far below it), and the STOP can be set on request count and seconds.

## What the series are (measured; this corrects my first cut)

- **Calendar-day, contiguous, from each account's roster start day.** The compact Daily breakdown is `basedOn Calendar`: one point per calendar day. All 9 series (4 + 5) are contiguous with no gap and begin on the account's roster start day (0 days after it). Weekend points are flat: 1,057 of the 1,088 weekend points have a factor of exactly 1, so chaining across calendar days is safe.
- **Chained daily factors reproduce Orion's own period return for periods up to a year, exactly (0.00 bp), on all 7 series up to a year.**
- **Over a year Orion ANNUALIZES the summary return** (`annualize` is on in the request). The 2 multi-year series (686 and 2,228 days) match the summary only after the 365/span annualization (residuals within 10 bp: about 0.9 and 6.2 bp). **So the feed must store the DAILY FACTOR and let the adapter chain it for a since-inception or longer window; the summary value of a window longer than a year is annualized and must NOT be taken as the cumulative return.** (Alternatively the backfill request could turn `annualize` off; that changes the request body, which is the CTO's to rule.)
- **Two series END early:** the 686-day series ends 120 days and the 2,228-day series ends 95 days before 2026-10-13; the other 7 end on that date. These are accounts whose Orion series stops months before the pull date. This is the best explanation so far of round 118's "group with no series over Q3, with a series over YTD": the series stops before the Q3 window. I did not match these two series to the accounts whose positions Opal holds to the end date (round 117 read), so whether Orion's series is stale for an account that is still open is NOT established here. The cause of the early end is not read. For the feed: days after a series ends must be `ABSENT` with its own reason class (suggest `SERIES_ENDED_AT_SOURCE`), never a carried-forward or zero return.
- **The 2 accounts with no group** (one in each household) are the null-start-date accounts of rounds 119 and 120, as expected.

## What this seat read for itself

I re-ran the criterion in the worker's tree (PASS), re-validated the proof instance (VALID), merged through `safe-merge.sh` (the first attempt was refused because `2.0.0_SA_COO~D2` had an uncommitted append in the shared channel file; I waited and retried clean), scanned the changed files for identifier-length digit runs (none: the flagged runs are a short commit hash and two numbers of the bound) and computed the series spans, gaps, the cumulative and annualized chains and the weekend flat-factor counts from the private bodies myself, printing no value. **Not a grade.**

## Issuer errors this round (mine, disclosed)

1. **The worker's worktree was a sparse checkout** without the loader modules; the worker stopped before any call (row `W309-S1`). I added four directories to its sparse set and a fifth (`_ids`, imported by `tenants.py`) after a test import. I had not checked what `wk-provision.sh` produces now.
2. **My first-cut checker rules were wrong:** completeness in NYSE trading days and every series chained against the summary. The probe showed the series are calendar-day and the summary is annualized over a year. The worker's note that annualization was "tested and rejected" was also wrong on my recomputation; the fault in both is mine for the rule. Amended @8146c5c082; the stale record failed the amended check and the worker recomputed from its saved bodies, no new call. **The 10 bp tolerance for the annualized reading is mine, set after seeing residuals of about 1 and 6 bp**; the packet reports the residuals so the tolerance is not the finding.

## Rows held (owners named)

`W309-S1` (BLOCKING, INERT: ruled and resolved), `W309-S2` and `W309-S3` (INERT: ruled by the amendment). No ARMED row from this round. `D2-S60` and `D2-S61` stay on the feed landing.

## What goes to the CTO and `~P2`

1. **The bound above** goes into pair (b) ADDENDUM 2 as the STOP: 294 requests, 537 s serial, 337 MB ceiling.
2. **Store the daily factor, not the window summary,** for anything longer than a year (the adapter chains it); or the CTO rules `annualize` off for the backfill body.
3. **A new reason class for the feed:** `SERIES_ENDED_AT_SOURCE` for days after an account's series ends (2 of 9 series here).
4. The one-time run also fills the days the scheduled feed will never reach, so the account pages' QTD, YTD and last-12-month windows can be served from the first scheduled run onward, and the since-inception window from the chained factors of the full history.

## What this does to the FWD outcomes

Inputs to `FWD-2` for Inflection: closer. The history exists and is usable; the feed and its backfill are `~P2`'s build and apply. The account pages stay "Account-level returns are not available for this firm yet." until they land and the adapter reads them.

## Open

**Andrew:** nothing from this workstream. **This seat:** the adapter cell is cut when the feed lands its first bronze and silver, and reads the history the backfill writes.

-- 2.0.0_SA_COO~I2
