# NEVER-WIDEN SIGN-OFF -- the COO half. `chatter_event` gold rebuild under the amended `C-HV-EVENT-SPINE`

**Signed by:** `2.0.0_SA_COO~Y`, 2026-09-28 ~10:5xZ. **Counterpart owed:** `1.0.0_SA_CTO~Z` (its 20260928T102818Z
asked for my half first). **Act:** round 11 cell 1 -- rebuild the `chatter_event` gold table so the served event
set reflects the amended rule (publishers counted over tier-A only).

⛔ **THIS HALF NAMES THE ACT'S BLAST RADIUS AND THE ROLLBACK PER KEY. It is not a restatement of the producer's
decision.**

## 1. WRITERS OF THE NAMED PROPERTY -- **N = 1**, and N is printed because the rule requires it

`write_gold(GOLD_EVENT_TABLE, ...)` at `lib/research/harvest/publication_gold.py:914`, reached only from
`build_event`. **One writer, so ONE rule read.**

**Measured, whole repo:** `comp-find 'GOLD_EVENT_TABLE|chatter_event'` -> 197 hits / 76,962 files
(DEF 1, SURFACED 53, CONFIG 28, DOC 115). The only WRITE is `:914`. `timeline_api.py` states in its own header
that it *"never builds or writes `chatter_daily`/`chatter_event` ... it only SERVES"*.
⚠ **My first census of this used `\(` and `\|`, which python `re` reads as LITERAL** -- the comp-tool warned, and
a wrong N would have voided this half. The count above is from the corrected bare-pipe pattern.

⭐ **AND THERE IS NO SCHEDULED PRODUCER.** The CONFIG band is entirely evidence, inventory and proof-of-spec
files -- no Lambda, no cron, no EventBridge rule writes this table. **So NEVER-1's specific override hazard --
"a `--month`-style override that lets a scheduled producer run off its own clock creates a new reachable state on
the manual path" -- DOES NOT APPLY: there is no scheduled path to race.** (Separately notable: this gold has only
ever been built ad-hoc, which CLAUDE.md permits for QA while requiring production pipelines to be scheduled. Not
this act's business, but it is the reason the hazard is absent.)

## 2. WHAT THE ACT MAY TOUCH -- read from the producer's rule, not from the input's shape

`write_gold`'s own docstring and body: *"ONE conditional put (never-overwrite precondition) of a full parquet
snapshot, then a read-back (HEAD + length match). The `date=` partition is the BUILD date, not any row's own
date -- each build is a full snapshot."*

- **The put carries `IfNoneMatch="*"`.** ⛔ **So the act CANNOT overwrite an existing object.** It creates ONE new
  key: `amgt/harvest/gold/chatter_event/date=<BUILD date>/part-<run_stamp>.parquet`.
- **Every prior snapshot is untouched** -- including the current 12-row one. Nothing is mutated and nothing is
  deleted.
- **BLAST RADIUS: exactly one new S3 object.** No other table, partition or key is written. `chatter_daily`,
  `article_security_mention` and silver are not touched by this act.

## 3. BOTH BRANCHES, because a half that covers one is not signed

| branch | what the PRODUCER's rule does | served state after |
|---|---|---|
| **SUCCESS** | put succeeds, then `head_object` and `ContentLength == len(body)` must match; returns `{uri, bucket, key, rows, content_length}` | the new snapshot is the newest; readers (which take the NEWEST) resolve to **8 events** |
| **KEY COLLISION** | `IfNoneMatch="*"` makes S3 raise `PreconditionFailed` | **NOTHING is written. The 12-row snapshot remains the newest.** No partial state |
| **READ-BACK MISMATCH** | raises `store.HarvestStoreError` naming the bucket/key and both lengths | the object EXISTS but is declared bad by the producer itself. ⚠ **This is the one branch that leaves a served object the producer distrusts, and it is why section 4's rollback matters** |

**The expected SUCCESS outcome, read from the rule rather than predicted:** `rows` = **8**, from 12, with the 4
spurious events absent and 2 spans narrowed to new `event_id`s (`BA` 09-07..08 -> 09-08, `HD` 08-17..20 ->
08-18). `HVST-y-1` proved that diff in memory over the same landed mention rows, and proved
`C-HV-GOLD-REBUILDABLE` (two builds from one input are identical).

## 4. ROLLBACK PER KEY -- and it is NOT a delete, which is the point

⛔ **THE OBVIOUS ROLLBACK IS FORBIDDEN.** Readers resolve to the NEWEST snapshot, so "undo" would mean removing
the new object -- and **an S3 delete is a CLAUDE.md NEVER line requiring Andrew's word, and this project carries a
STANDING absolute clause against it** (decomp `s.14a`, after a sibling project's breach: no cell deletes an
object, a noncurrent version, or a delete marker).

**SO THE ROLLBACK IS FORWARD-ONLY, and it is sound rather than a hope:**
1. Revert the one-clause amendment to `event_rows` (it is one predicate; `HVST-y-1`'s commit isolates it).
2. Re-run the build. It writes a THIRD snapshot, newer than the 8-row one, carrying the **12** rows again.
3. Readers resolve to newest -> the prior partition is restored **by addition, never by deletion.**

**This is only sound because `C-HV-GOLD-REBUILDABLE` is PROVED, not assumed** -- a rebuild from the same silver
reproduces identical rows, measured twice byte-identical by `HVST-y-1`'s AC2. **If that property failed, this
rollback would not exist and I would not sign.**

⚠ **THE READ-BACK-MISMATCH BRANCH uses the same rollback**, with one extra statement: the distrusted object stays
in place (we may not delete it) and is superseded by the rebuild. **Anyone auditing the partition later will see
three snapshots and must take the newest** -- that is the existing reader rule, not a new one.

## 5. WHAT THIS HALF DOES NOT COVER

- **It is not a vendor word.** The rebuild reads landed gold and silver; it makes no publisher request. `w-2`,
  `w-4`, `w-5` stay carded at Andrew.
- **It does not cover `chatter_daily`.** If the rebuild is ever widened to that table, this half does not reach it
  and a new pair is owed.
- **It does not authorise a delete, a version removal, or a delete-marker removal** -- under any circumstance,
  including a failed read-back.
- **It does not cover a PUSH of the portal DEV merge.** That waits on Andrew's word per the round-10 analysis.
- **It grades nothing.** `HVST-y-1`'s AC4 is `3.0.0_SA_CVO`'s at L9; FWD realization is the CTO's at L10.
