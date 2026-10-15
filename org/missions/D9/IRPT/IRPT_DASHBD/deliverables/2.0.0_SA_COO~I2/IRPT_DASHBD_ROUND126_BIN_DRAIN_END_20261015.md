# IRPT_DASHBD round 126, workstream B-IN (Inflection) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-15 ~22:5xZ)

**One order (a LOCAL read), drained and graded on the LANDED tree; no vendor call, no write to AWS, nothing deployed; the bodies and the positions extract stay in the private folder; counts, verdict words and digests only in the repo, and no date.** Issued @b8b717d5a5 (merged @768ab85a86), check amended @47c68a361a (merged @19d5b8214a), drained: `DB-i-13` (~313, merged @3e9df877fd). On the merged tree `DBI126-1-AC1` PASSES and the proof instance reads VALID. `round-close-check --project IRPT_DASHBD --round 126 --workstream B-IN` reads **MAY-CLOSE** (1 order, 0 judgment criteria). Push state: LOCAL on box/dell2, not read against origin. Cut on the CTO's round-122 analysis item 3 and ADDENDUM 1 (msg 8678).

## The finding: neither early-ending series is stale at source

Of the 9 Account series in the two saved round-122 bodies, 2 end before the window end. Compared with Opal's own `fact_positions` silver (a GET-only read, 120 reads, cap 200, 0 writes, 0 vendor calls):

| early-ending series | ends before the window end | positions partitions after it | held on how many | held on the newest | verdict |
|---|---|---|---|---|---|
| account 1 | 95 days | 95 | 0 | no | `CLOSED_OR_TRANSFERRED` |
| account 2 | 120 days | 117 | 1 | no | `CLOSED_OR_TRANSFERRED` |

Verdict counts: `STALE_AT_SOURCE` 0, `CLOSED_OR_TRANSFERRED` 2, `NOT_DETERMINED` 0. **So the feed's `SERIES_ENDED_AT_SOURCE` days correspond, in this sample, to accounts Opal no longer holds, not to a live account whose Orion series went stale.** What it does not establish: the sample is 2 accounts of 9 series in 2 households; a position held on one day after the end (account 2) is a single partition, not a holding; and the cause of the closure or transfer (a real close, a custodian move, a re-registration) is not read here. The row `D2-S91` (disarm owner `~P2`) can cite this; the full-universe read is the feed's own first data.

## What the issuer read for itself

Re-ran the criterion in the worker's tree (PASS) and on the merged tree (PASS), re-validated the proof instance, merged through `safe-merge.sh` (the first attempt lost the race to other seats' commits three times and landed nothing; I re-ran it and it landed), scanned the changed files for identifier-length digit runs (none outside a hash, a private path and a task-order header), and **spot-read the newest `fact_positions` partition myself** (1 LIST and 1 GET beyond the worker's): both early-ending accounts read not held on it, as the record says. **Not a grade.**

## Issuer error this round (mine, disclosed)

The first run of `DBI126-1-AC1` read FAIL for a fault in MY checker: its identifier scan did not exempt the record's private `extract.path`, although the order names path and file fields as exempt. The worker stopped, reported it as a BLOCKING row (`W313-S1`) and did not edit the checker or the path. I amended the check (blank those two fields before the scan, keep the rule elsewhere; two new selftest arms; the nine bad variants still FAIL), put it on the worker's branch and resumed the worker, which re-ran the criterion with no new read.

## Rows

`W313-S1` (BLOCKING, ruled by the amendment) and `W313-S2` (INERT, reconciles S1): both closed. No ARMED row from this round.

## Open

Round 127 (the module on contract 0.4.2) is in flight with worker ~314. The first real-row run waits on `~P2`'s apply of the feed (IB-pr-596).

**Andrew:** nothing from this workstream.

-- 2.0.0_SA_COO~I2
