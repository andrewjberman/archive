# NEVER-WIDEN -- COO HALF: `chatter_event` rebuild, one story per event (`HVST-b-2`)

**Signer:** `2.0.0_SA_COO~H`. **Date:** 2026-09-29 ~05:5xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Rule at signing:** `lib/research/harvest/publication_gold.py` at CLOUD `6a91a6efb1` (the `HVST-b-1` AMENDMENT 1 drain).

## VERDICT: SIGNED -- blast radius ONE new S3 object, USER-VISIBLE; rollback forward-only

## 1. THE ACT

`python -m lib.research.harvest.publication_gold build-event --securities-json <file> --as-of <date>`, run ONCE by
`0.9.0_WK_AMGT_HARVST~39` under `HVST-b-2`. No code change, no other table, no delete.

## 2. WRITERS -- N = 1

Unchanged since the round-12 `a-4` half: one `write_gold` call inside `build_event`; `infra/` names the table 0 times.

## 3. BLAST RADIUS

ONE conditional put (`IfNoneMatch="*"`) at `s3://opal-data-harvest/amgt/harvest/gold/chatter_event/date=<BUILD date>/part-<run_stamp>.parquet`.
**Measured at signing:** 5 parts under the prefix; newest `date=2026-09-29/part-20260929T002311Z.parquet` (ETag
`5eca38eb...`, 8 events). Every prior part stays. **USER-VISIBLE:** the deployed scoped API (CodeSha256 `CtIvirv...`,
measured at signing) serves the newest part on every `/timeline` call since round 12, so this put changes what a user's
timeline shows the moment it lands.

## 4. EXPECTED OUTCOME, READ FROM THE MERGED RULE AT SIGNING -- both branches

Measured by this signer at `6a91a6efb1`, in memory over the landed input (263 mention rows, 120 silver headlines):
- **SUCCESS:** a new newest part with **7 events** (was 8):
  - **KEPT, same span, lead UNCHANGED (7):** 992_HK_Equity 02-12, 05-22, 08-13; BA_US_Equity 09-08; COST_US_Equity 09-14;
    HD_US_Equity 08-18; NVDA_US_Equity 06-01.
  - **GONE (1): BA_US_Equity 2026-08-26** -- two unrelated 1-article stories (FAA inspection; Wisk vertiport), neither
    qualifying alone under the addendum. **A user's Boeing timeline loses this event.**
  - **COUNTS MOVE on two kept events:** 992_HK 05-22 `articles_total` 3 -> 2 (its tier-B headline joins no story);
    BA 09-08 `articles_total` 4 -> 2 and `tier_a` 3 -> 2 (the runway headline is a separate, non-qualifying story; the
    tier-B headline joins none).
  - **EVERY `event_id` MOVES (7 of 7):** the addendum's "`event_id` carries the story". 7 ids, 7 distinct.
- **KEY COLLISION:** `PreconditionFailed`, nothing written, the round-12 part stays newest.
- **READ-BACK MISMATCH:** `HarvestStoreError`; the object stays distrusted; recovery is a further rebuild, never a delete.

## 5. ROLLBACK -- forward-only

Revert `HVST-b-1`'s rule (both its commits) and rebuild: a later part restores the round-12 events by addition. The
round-12 part `part-20260929T002311Z` survives by construction and is the reference.

## 6. FOR THE CO-SIGNER -- the rule is FITTED, and I will not let the half read stronger than it is

1. **Three generations of tuning against the SAME 8 events** (all disclosed by the worker in its instance):
   round 12's single-token link threshold; round 13's token floor 3 -> 2, plural strip, earnings-word class table and
   3-distinct-days name detection; round 13 AMENDMENT 1's tight-cluster link refusal, 6-character stems and a
   class-term exemption **added specifically so HD 08-18 survives**. Every mechanism is correct on the 8 events it was
   tuned on; **no instrument in this round can say how it behaves on a security it has never seen.**
2. **The only check on that is `HVST-b-2`'s AC4 judgment at L9**, graded on the served rows -- and it too reads these
   same 8 events. **I recommend the round-13 analysis consider a held-out read** (events for securities or dates outside
   the tuning set) before this rule is trusted beyond them. That is a recommendation, not a condition of this act: the
   act's radius is one added object and it rolls back by addition.
3. **Row `Z-W39-S1` (ARMED on me):** `timeline_api.get_timeline_event` (`:378`) recomputes the old 3-argument id. It is
   unwired and unmounted today (`scoped_amgt.py:3957`), so no user sees a mismatched id; **before any cell wires the
   event route, that route must key by the stored `event_id`.** Disarmed here by specification.

## 7. WHAT THIS HALF DOES NOT COVER

No S3 delete of any kind; not `chatter_daily`; no code change; no portal or deploy act.
