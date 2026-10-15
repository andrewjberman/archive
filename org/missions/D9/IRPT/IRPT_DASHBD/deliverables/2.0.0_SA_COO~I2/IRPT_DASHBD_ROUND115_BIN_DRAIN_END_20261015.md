# IRPT_DASHBD round 115 (the CTO's B-IN analysis, msg 7956), workstream B-IN (Inflection) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-15 ~03:1xZ)

**One order, drained; nothing served moved, nothing written to AWS, nothing deployed; counts, bp and shares only in the repo; the transactions frame, the cache and the per-household table stay in the private folder `C:/dev/_irpt_private_evidence_20261009/`.** Issued @3ddb11e9f7 (merged @0350c67cdc). Drained: `DB-i-3` (~303, @5540cb2803). On the landed tree `DBI115-1-AC1` PASSES and the proof instance reads VALID. `round-close-check --project IRPT_DASHBD --round 115` reads **MAY-CLOSE** (3 orders in round 115 across workstreams, 0 judgment criteria: nothing here is for the CVO to grade by eye). Push state: LOCAL on box/dell2, not read against origin.

## What the cell found

The sample is 12 households by the rule (all 9 at 100 bp or more, and the lowest-hash household of each other bin: 1 under 5, 1 at 5 to 25, 1 at 25 to 100). **Both controls hold: `base` equals round 114's `all` gap on 12 of 12 households, and the `identity` variant equals `base` on 12 of 12.**

| difference | variant | status | households computed | closer to Orion | median share |
|---|---|---|---|---|---|
| gross against net of fees | `gross_fees` | TESTED | 12 | 11 | 0.26 |
| flow timing inside a day | `flow_start_of_day` | TESTED | 12 | 9 | 0.10 |
| flow timing inside a day | `flow_midday` | TESTED | 12 | 6 | 0.03 |
| the cash sweep | `ex_cash_value` | TESTED | 11 | 3 | 0.00 |
| the cash sweep | `ex_cash_no_flows` | TESTED | 11 | 4 | -0.07 |
| trade against settlement date | `settle_timing` | NOT_TESTABLE | 0 | - | - |
| income accrual | `income_accrual` | NOT_TESTABLE | 0 | - | - |

**Reading.** No single difference explains the gap across the sample. Fees counted gross is the most consistent: it moves 11 of 12 households closer, but by a median of about a quarter of the gap. Start-of-day flow timing moves 9 of 12 and a median tenth. The two cash-sweep forms do not help (they move a minority closer, and the second widens the median household's gap). **The record's count of "households where a single difference explains half" is 10 of 12, and it overstates what it sounds like:** it counts the largest share per household, and shares above 1 (an overshoot past Orion's figure) count: 1 household under `gross_fees` (one share reads 36, on a household whose baseline gap is tiny), 3 under `flow_start_of_day`, 5 under `flow_midday`, 1 and 3 under the two cash forms. Read it as "a difference moves that household past half of its gap", not as a cause found. A household-level reading needs the signed shares in the private table, which stay private.

**Two of the five differences cannot be tested from Orion's own data.** The newest `fact_transactions` partition carries 36 columns and none is a settlement date, an ex-date, a record date, a pay date or an accrual date, so `settle_timing` and `income_accrual` are NOT_TESTABLE (an absent fact, not a zero). The frame does carry `executionTime` and `pull_date`; neither is a settlement date.

## What this seat read for itself

I re-ran the criterion in the worker's tree (PASS), re-validated the proof instance with the worktree's own checker (VALID), merged through `safe-merge.sh` (row gate on the merged index: 0 violations; one first attempt was refused while `2.0.0_SA_COO~Y2` held an open merge, then re-run clean), and scanned the three files the worker added for identifier-length digit runs outside a hash, a private path and a date: none. The checker recomputes the sample, the baseline, the identity control and every share from the private table. I did not open any household's values. **Not a grade.**

## Issuer errors this round (mine, disclosed)

1. My feed harness for the check showed a defect in the check before the cut (a digest list under a key without `sha256` in its name tripped the identifier scan); fixed before the cut.
2. The seat row `D2-S52` I filed carries a `surfaced_at` of 03:05Z typed by hand, about 12 minutes ahead of the commit time; the row gate warned. The row is append-only; the real time is the commit's.
3. After the first merge attempt was refused, my command still removed the worker's worktree. The branch and its three commits were intact (verified before the retry), and the retry merged them.

## Rows held (owners named)

`W303-S1` (ARMED, owner this seat): the commit gate's client account-id check did not run on dell2 because the hashed list is absent. It is the same condition as `W182-S1` (ARMED, owner `0.0.0_AB_MSTR`, infrastructure); `D2-S52` records this seat's scan as the stand-in and carries it as INERT for this seat. No ARMED row has a dark owner here.

## What goes to the CTO

The tolerance cannot be ruled on this read: the gap is a mix, and the two differences most often named for it (settlement timing, income accrual) are not testable from the Orion feed. Options for the next cell, none cut: (a) a COMBINED test on the same 12 households (gross fees plus start-of-day flow timing together), since each moves most households closer by a fraction; (b) a read of Orion's own definition of its client factor (net or gross of fees, how it treats a flow inside a day), which would settle (a) without a search of variants; (c) nothing at account grain: `fact_performance` carries only client, date and factor (row W172-S3), so any account-level tie-out needs a source Orion's feed does not hold. Which of (a) and (b), or neither, is the CTO's call.

## What this does to the FWD outcomes

Inputs to `FWD-2` (account-level returns for Inflection): not met. The account pages stay "Account-level returns are not available for this firm yet." and the windows over 2026-07-01 and 2026-09-28 carry `SOURCE_BREAK` words until `~P2`'s re-pull lands.

## Open

**Andrew:** nothing from this workstream. **This seat:** the next B-IN cut waits on the CTO's round-116 B-IN analysis.

-- 2.0.0_SA_COO~I2
