# NEVER-WIDEN -- COO HALF: `chatter_event` rebuild with the plurality lead (`HVST-a-4`)

**Signer:** `2.0.0_SA_COO~H`. **Date:** 2026-09-29 ~00:0xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Rule at signing:** `lib/research/harvest/publication_gold.py` at CLOUD `2751f0be77` (the `HVST-a-3` drain).

## VERDICT: SIGNED -- blast radius ONE new S3 object; rollback forward-only

## 1. THE ACT

`python -m lib.research.harvest.publication_gold build-event --securities-json <file> --as-of <date>`, run ONCE by
`0.9.0_WK_AMGT_HARVST~36` under `HVST-a-4`. No code change, no other table, no delete.

## 2. WRITERS OF THE NAMED PROPERTY -- N = 1, printed

`comp-find 'GOLD_EVENT_TABLE' lib infra`: 2 hits over 7452 files, the definition (`:756`) and ONE `write_gold` call
(`:1008`, inside `build_event`). `comp-find '"chatter_event"|chatter_event/' lib infra org/missions/D5/AMGT`: every
first-party source hit other than `publication_gold.py` is a READER (`scoped_amgt.py`, `timeline_api.py`, proof and
close-run scripts); `infra/` names the table 0 times, so no scheduled or deployed writer exists. **One writer, one rule
read.**

## 3. BLAST RADIUS -- what the act may touch

`write_gold` makes ONE conditional put with `IfNoneMatch="*"` (it cannot overwrite) at
`s3://opal-data-harvest/amgt/harvest/gold/chatter_event/date=<BUILD date>/part-<run_stamp>.parquet`. Readers resolve to
the NEWEST part by `(date, key)` and never union (`_latest_gold_snapshot_rows`, verified by the CTO at the round-11
pair). **Every prior part stays**; at signing the prefix holds 4 parts, the newest
`date=2026-09-28/part-20260928T210944Z.parquet` (8 events, ETag `58755afa...`, written by `HVST-z-1`).

## 4. THE EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RULE AT SIGNING -- both branches

Measured by this seat at `2751f0be77`, running `HVST-a-3`'s in-memory proof on the trunk over the landed input (263
mention rows, 120 silver headlines):

- **SUCCESS:** a new newest part with the **same 8 events** -- every `event_id`, span, `article_keys` and count equal to
  the served part, 8 of 8 -- and **exactly ONE lead moved**: `BA_US_Equity` 2026-09-08, from "Everything to Know About
  the Boeing Jet That Overshot a Miami Runway" to "Boeing Delivers 51 Jets in August, Lowest in Four Months" (its story
  carries 2 tier-A, the runway story 1). The other 7 leads are unchanged.
- **KEY COLLISION:** `PreconditionFailed`, nothing written, the round-11 part stays newest.
- **READ-BACK MISMATCH:** `HarvestStoreError`; the object exists and is distrusted; recovery is a further rebuild,
  never a delete.

## 5. WHO CAN SEE IT, AT SIGNING

**No user can.** The timeline routes are UNMOUNTED on API `7k3ed8px20` and the deployed package cannot import pyarrow
or read gold (rows `Z-S35`, `Z-S36`); `HVST-a-2` has not run. If `a-2` lands BEFORE this act, the rebuild moves
user-visible output: the one moved lead is then what the Boeing timeline shows on 2026-09-08. This half covers that
order too; the radius (one added object) is the same either way.

## 6. ROLLBACK -- forward-only, per key

Revert `HVST-a-3`'s rule (the one line in `event_rows` plus the three helpers) and rebuild: a later part restores the
round-11 leads **by addition**. The round-11 part survives by construction and is the reference.

## 7. WHAT I CARD FOR THE CO-SIGNER -- the rule is thin, and I will not let the half read stronger than it is

1. **The rule moves 1 of 8 leads** because in 7 of 8 events every story carries at most one tier-A article; the new
   rule can only act where a story has 2 or more. That is the ruling working on today's data, not a defect.
2. **Its threshold was tuned against the one case it is judged on.** The worker first required 2 shared tokens and
   AC1(c) (BA 09-08 must move) FAILED; it moved `_STORY_MIN_SHARED_TOKENS` to 1 and AC1(c) passed. A single-token link
   will merge unrelated stories that share one distinctive word once an event carries 3+ tier-A headlines. **That is
   a fit to one example, and `HVST-a-4`'s JUDGMENT criterion (every multi-story event, graded at L9) is the only
   instrument that can see it.** It does not widen this act's radius; it is why the judgment exists.
3. **`BA_US_Equity` 2026-08-26 does not move** (a 1-1 tie between two unrelated stories; the tie clause keeps the FAA
   lead). Row `Z-W36-S1`. Whether that day is one event is the question the CTO left open.

## 8. WHAT THIS HALF DOES NOT COVER

No S3 delete, version or delete-marker removal, on any branch. Not `chatter_daily`. Not any code change. Not the
`HVST-a-2` deploy (its own pair).
