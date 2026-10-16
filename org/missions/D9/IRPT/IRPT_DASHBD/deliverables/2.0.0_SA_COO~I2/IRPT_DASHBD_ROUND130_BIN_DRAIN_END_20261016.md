# IRPT_DASHBD round 130, workstream B-IN (Inflection) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-16 ~00:3xZ)

**One direct-act order (a one-condition edit and its tests), drained and graded on the LANDED tree; no vendor call, no S3 write, nothing deployed, no client data.** Issued @f71ea6eefc (merged @d9e8307c5d), drained: `DB-i-17` (~317, merged @cfa6dcab48). On the merged tree `DBI130-1-AC1`, `AC2` and `AC3` PASS, 64 tests pass across the adapter and wrapper test files (35 + 29), and the proof instance reads VALID. The round-129 run script's criteria (`DBI129-1-AC1` to `AC3`) still PASS on the same tree. `round-close-check --project IRPT_DASHBD --round 130 --workstream B-IN` reads **MAY-CLOSE** (1 order, 0 judgment criteria). Push state: LOCAL on box/dell2, not read against origin. Cut on the issuer's own defect (no CTO analysis); the CTO's round-129 analysis (msg 8779) already names the 48-row refusal and accepts the fix.

## What changed

The wrapper's partition check compares each row's `day` with its partition `date=<d>` (it compared `pull_date`). A row whose `day` is not its partition's is refused with a count and nothing written; a `pull_date` that differs from the partition is accepted. The refusal message now says the rows "name a day other than their partition's". One test moved to the new rule and one test was added for the backfill shape.

## Confirmed on the feed's own writer (beyond the checker's fixture)

I ran the feed's own `run()` over its own offline fakes (the feed's test harness) for a three-day backfill window: it writes three silver partitions, one per day, with `pull_date` the pull day on every row. The pre-fix wrapper refused them (10 rows in that run); the fixed wrapper accepts them and writes 15 rows (5 accounts x 3 trading days), 1 PRESENT and 14 ABSENT, 0 trading days unaccounted. So the defect was real and the fix matches the real writer, not only my fixture. Round 131 (`DB-i-18`) makes that permanent: its tests build their partitions only by running the feed's own `run()` (the CTO's rule, msg 8779).

## What the issuer read for itself

Re-ran the three round-130 criteria and the three round-129 criteria on the merged tree (PASS), both test files (64 passed), the proof, and the wrapper diff (4 changed lines: the condition and its message). **Not a grade.** The first merge attempts lost the lock to other seats' merges; a retry landed.

## Rows

Worker rows `W317-S1` (the module docstring still describes the round-125 pull-date rule; the order said nothing else in the file changes) and `W317-S2` (a partition whose rows carry differing or null pull dates is accepted; no test covers it): both INERT. S1 is a one-line docstring fix I will batch into the next wrapper order; neither is armed.

## Open

Round 131 (the feed-writer fixtures as a criterion) is being cut. The first real run waits on `~P2`'s apply of the feed (IB-pr-596), then the backfill; the page reader after.

**Andrew:** nothing from this workstream.

-- 2.0.0_SA_COO~I2
