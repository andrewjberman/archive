# The issuer's own re-run for row IRPT_DASHBD-D2-W111-S1: five of five days reproduce to the cent

**By:** 2.0.0_SA_COO~D2, 2026-10-11 ~19:4xZ. **Ordered by:** 1.0.0_SA_CTO~DELL2's ROUND-75 ANALYSIS
(`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_DASHBD_ROUND_75_20261011.md` @06b01d9b88, item 1): "Your own re-run, on
five of the 50 days you choose yourself, across at least three of the 18 segments: each transaction id counted once, against the served
day flow, to the cent. Five of five closes row D2-W111-S1; a miss re-opens the 18."

## What was claimed

Worker `0.9.0_WK_IRPT_DASHBD~113` (DB-b-140, record `deliverables/0.9.0_WK_IRPT_DASHBD~113/UNREPRODUCED_18.json`): the custodian's
transactions copy lands a transaction once per portfolio group; counting each transaction id once, the ledger day total equals the
served day flow to the cent on 50 of 50 differing days.

## What this seat did, and did not take from the worker

- Taken from the worker: ONLY which (segment, account, day) triples are the 50 (its private `a1_days.pkl`), sorted by segment then day.
- Chosen by this seat before any read: positions 3, 14, 27, 38 and 46 of that order (zero-based). They fall in 5 different segments.
- Read fresh by this seat, from S3, not from any worker's file:
  - the served day flow: 5 served `account_return_daily` day partitions of 49 Financial, the `external_flow` column for the account;
  - the custodian's copy: all 1,878 date prefixes of 49 Financial's Black Diamond transactions tree, 1,878 objects, filtered to the
    chosen accounts and days and to the two external-flow kinds.
- Reads only. 0 writes. No value left the private folder: the script printed counts and booleans.

## Result (counts and booleans only)

| day | segment | ledger rows | distinct transaction ids | copies per id | portfolio groups on the day | naive sum equals served, to the cent | each id once equals served, to the cent |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 4 | 1 | 4 | 4 | no | yes |
| 2 | 2 | 8 | 2 | 4 | 4 | no | yes |
| 3 | 3 | 6 | 1 | 6 | 6 | no | yes |
| 4 | 4 | 4 | 1 | 4 | 4 | no | yes |
| 5 | 5 | 3 | 1 | 3 | 3 | no | yes |

**Five of five reproduce to the cent with each transaction id counted once; none of five does with the naive sum.** Every one of the 25
ledger rows carried a transaction id, and on each day the number of copies of an id equals the number of portfolio groups present.

## What this does and does not establish

- It establishes, on a read independent of the worker's download and of its code, that the worker's cause holds on 5 days in 5 of the
  18 segments. By the CTO's stated rule that closes row D2-W111-S1.
- It does NOT re-establish the other 45 days: those rest on the worker's read.
- It does NOT touch the contested flow-timing question: the 51 stay contested, and the tie-out is not closed.
- The served side was read from the served gold, which is the thing the tie-out judges; the producer's rule for building it was not
  re-read by this seat.

Script and its result file, outside the repo: `C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/2.0.0_SA_COO~D2/rerun_five_days.py`
and `rerun_five_days.result.json`.

-- 2.0.0_SA_COO~D2
