# NEVER-WIDEN -- COO HALF: the served silver re-derivation (FWD-2, round 45 HVST-ar-1)

**Signer:** `2.0.0_SA_COO~H`, 2026-10-04 ~22:5xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Authority:** round-44 analysis @ed9efe80ea, ruling 1 and enrichment item 1. Decomposition section 58. Builder merged
@38fc65b7bf (worker ~93's @eab4321d38, plus the Z-W93-S1 pin disarm @ccb21d1a4e).

## WHAT THIS HALF SIGNS: A PLAN BY ITS DIGEST, AND THE RULE THAT PRODUCES IT

The act is `round45/ar-1.rederive_act.py`. `--write` re-runs the identical plan and refuses unless the plan's digest equals
**`9d7b7d57c651eb76067a286ce1a77b08dd92c432271a6a3b45ab0836bb0061b4`**. After writing, it re-reads served silver and requires
every planned row to be the row its `article_key` now serves.

**THE RULE** (the act's module docstring):
- A served row is chosen by `store.supersedes`, the rule every silver reader shares.
- A stored original is rebuilt only when it IS its article's served row and its `record_hash` differs.
- An original whose article has no served row is added as a new row.
- An original that is another fetch of a served article is never planned.
- Rows are appended per fetch date in type-compatible bins, one `silver_append` call per bin, through the uploader's own
  `_silver_append_retrying_object_name`. Every bin uses the batch `run_stamp`, the greatest stamp among the parts it
  supersedes, so each new part name sorts at or after every part it replaces. A name collision takes `-rN`, which sorts
  after its base.

## Measured at signing (dry run 2, 0 writes)

Source: `round45/ar-1.rederive_dryrun.out`, `ar-1.rederive_plan.json`.

| publisher | originals | rebuilt | new | unchanged | other fetch | CHANGED | GONE | errors | bins (rows) | parts superseded |
|---|---|---|---|---|---|---|---|---|---|---|
| barrons | 164 | 149 | 0 | 15 | 0 | 0 | 0 | 0 | 1 (149) | 1 |
| bbg | 1,277 | 1,245 | 2 | 30 | 0 | 0 | 0 | 0 | 4 (835, 3, 405, 4) | 607 |
| ft | 184 | 170 | 0 | 14 | 0 | 0 | 0 | 0 | 2 (168, 2) | 78 |
| wsj | 444 | 414 | 15 | 15 | 0 | 0 | 0 | 0 | 6 (11, 11, 307, 1, 97, 2) | 381 |

Rows written: 1,995 (1,978 rebuilt + 17 new) in 13 new parts. Gate: **HOLDS**.
- **CHANGED 0:** every pre-existing served column keeps its value. `record_hash` re-hashes by design, because columns
  are added.
- **GONE 0:** every rebuilt row keeps its `fetched_at`, so it supersedes in place.
- **Dry run 1 FAILED the gate:** one batch per date mixed bbg `duration` int with str, and wsj `caption` list with str
  (row Z-W93-S2). The bins exist because of that failure, and nothing was written.

## Writers of the served property (silver `article` for bloomberg, barrons, ft, wsj): N = 3

1. The collector's `HarvestUploader` (`upload-harvest`), on a collection run. None is running; the next one is the run per
   publisher that Andrew's lift allows, and it comes after this round.
2. `LegacyUploader`. It is not run.
3. This act.

The act never overwrites. Every put is `IfNoneMatch="*"`, so every pre-existing part stays byte-identical.

## What moves and what does not

- **Served silver:** 1,978 article rows gain columns only. 17 articles gain a first silver row: 2 bbg and 15 wsj
  originals that had none (11 were builder faults, now fixed; 6 were batch conflicts).
- **Gold is untouched by this act.** The next gold rebuild reads the new rows under its own pair. The 17 new articles can
  then add mention rows, and the record_hash change touches nothing gold keys on: the FinBERT tone joins by content key,
  and the scored text is unchanged.

## Rollback, per key

Delete the 13 new part keys, which the `--write` record (`ar-1.rederive_plan.written.json`) lists by name. The superseded
parts are untouched, so each article's served row reverts to exactly the row it serves today.

Not covered: any put outside the 13 parts the write record names, and any run whose digest is not the one above.
