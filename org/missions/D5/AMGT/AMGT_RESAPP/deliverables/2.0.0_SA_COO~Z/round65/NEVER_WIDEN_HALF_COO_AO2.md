# AMGT_RESAPP round 65 -- `AMGT-ao-2` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-03 ~18:1xZ

**The act (ONE):** redeploy `opal-amgt-scoped-api` at build commit `9a8cbd2c97`, or a descendant whose CONTENT-DIFF equals the list
below. Build and upload ONE artifact, then ONE code-only `safe-apply`; `memory_size` stays 1769.
- Executor: `0.7.0_AE_CloudOps~A`.
- Order: `task-orders/AMGT_RESAPP.TO-AMGT-ao-2.the-code-redeploy.md`.
- It carries `AMGT-ao-1` (drained `9f8f4ee4b6`): FWD-38 (b) title case at the producer. CTO round-64 analysis @504827836c ruling 1.

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `KQSA62c3Diw5XqjBeKKZc0ZTZuTnaaRBbhuEQHfOdXQ=` (round-64 leg 2, LastModified 2026-10-03T01:52:29Z) |
| function MemorySize | 1769 |
| artifact S3 VersionId | `.xFOZLD1X0znp_5COtZvp3UgWTBrw19p` (41,149,311 B, `s3://opal-313476888478-lambda-artifacts/research/opal-amgt-scoped-api.zip`) |

## THE FILE LIST (`--build-only` at `9a8cbd2c97`)

The build read rc=0, cold-start FATAL [], request-time break [], and isolated 3 of 3. Against `KQSA62c3...`:
`CONTENT-DIFF SUMMARY: files 355, IDENTICAL 353, CHANGED 2, ADDED 0, REMOVED 0`. The package is 253,729,070 B (96.8%, 8,414,930 B spare).

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | CHANGED | `AMGT-ao-1`, worker ~216 `d72eed67f7` | See the list below. |
| `lib/research/harvest/publication_gold.py` | CHANGED | 2.0.0_SA_COO~H `4d393e3521`, which empties `QUARANTINED_PUBLISHERS` (ANDREW-DIRECT ~17:3xZ, "Release any quarantine that may have been initiated in any capacity") | NONE through this function. See below. |

**`scoped_amgt.py` served effect:**
- Every all-caps served `display_name` is re-cased in `_clean_display_name`, the seam every name chain ends in.
- Declared acronyms (36) and legal forms keep their case.
- The all-caps share-class tails go.
- 5 cut names take an estate-held full name with its source cited (`deliverables/0.9.0_WK_AMGT_RESAPP~216/CUT_NAMES.md`).
- `name`, `name_source` and `display_name_source` are unchanged. A mixed-case name is served unchanged. No row, rank, score or key moves.

**`publication_gold.py`: why no served effect through this function.** The 9 sites that read the map are all builders:
- `run_record_spans`, `publisher_coverage` and `daily_rows`
- `_iter_all_listing_hits`, `_without_quarantined_jobs` and `build_daily`
- `_iter_latest_articles`, `build_mention` and `build_event`

The routes call only `_day_of`, `_latest_gold_snapshot_rows_cached`, `BACKFILL_FLOOR`, `_baseline`, `_event_id` and `GOLD_DAILY_TABLE`. The comp-find census of `publication_gold.` and its imports over `lib/research/api`, `coverage` and `timeline_api.py` gives 11 + 8 hits. COO~H measured the served timeline restored on the deployed function through the gold restore alone.

Any other changed file at build time is a STOP.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| upload | a new version of `research/opal-amgt-scoped-api.zip` (versioned) | the prior VersionId `.xFOZLD1X0znp_5COtZvp3UgWTBrw19p` |
| code-only `safe-apply` | the function's code only; memory stays 1769 | a code-only `safe-apply` with that VersionId, restoring `KQSA62c3...` |

## EXPECTED OUTCOME -- both branches

| check | base (deployed KQSA62c3) | after (local at 9a8cbd2c97, ~18:1xZ) |
|---|---|---|
| r65 c17 | NO: price 60 of 94 all-caps, chatter 61 of 95, 'MITSUBISHI UFJ FINANCIAL GRO' on both | YES: 0 of 94, 0 of 95; 'Mitsubishi UFJ Financial Group' on both |
| r64 c12 | YES | YES (one name x 3 securities; e.g. 'The Boeing Co', 'Valero Energy Corp') |
| r64 c9, c10, c11, c13, c14 | YES (round-64 close) | YES |

**Failure branch:** any of the following is a ROLLBACK per the table:
- c17 or c12 is not YES;
- any other check moves;
- a non-200 on a covered key's overlay, thesis, peers, timeline or collected/chatter.

## WHAT THIS HALF DOES NOT COVER

Any of the following in the plan is a STOP:
- a memory change;
- a store write or an S3 delete;
- a vendor call;
- an IAM, route or gateway change;
- any data-engineering operation (collector, schedule or gold write).

The act changes no collection (ANDREW-DIRECT ~17:3xZ).
