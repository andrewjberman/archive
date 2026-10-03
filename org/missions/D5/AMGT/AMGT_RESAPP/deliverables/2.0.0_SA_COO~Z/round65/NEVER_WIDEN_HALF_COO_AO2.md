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

## AMENDMENT 1 (2.0.0_SA_COO~Z, 2026-10-03 ~19:1xZ) -- RE-PINNED to `19cb3df089`, CHANGED 3

**Why:** 0.7.0_AE_CloudOps~A stopped at this half's condition 1 (msg 28947). At HEAD the build read CHANGED 3, not 2. The cause
is 2.0.0_SA_COO~H `fc5a0bf42d`, which deletes the publisher-quarantine mechanism (HVST-ak-4) from `publication_gold.py` and
`finbert_sentiment.py`.

The ANDREW-DIRECT ~18:xxZ record (`ANDREW_DIRECT_20261003_18xxZ_DELETE_AGENT_TOS_CONTEXT_AND_UNAUTHORIZED_GATES.md`) orders,
verbatim, "all quarantine mechanisms, gates, or anything else that was implemented without my authorization" removed. The
original pin `9a8cbd2c97` still carries that mechanism, inert. **Issuer ruling:** the act ships the repo as it stands, at the new
pin. The original pin is withdrawn. AE~A recommended the same (msg 28949).

**THE BASE, re-read live ~19:1xZ, unmoved:**

| property | value |
|---|---|
| function CodeSha256 | `KQSA62c3Diw5XqjBeKKZc0ZTZuTnaaRBbhuEQHfOdXQ=` |
| function MemorySize | 1769 |
| rollback VersionId | `.xFOZLD1X0znp_5COtZvp3UgWTBrw19p` |

**THE FILE LIST (`--build-only` at `19cb3df089`, by this seat, in a clean worktree):**
- rc=0; cold-start FATAL []; request-time break []; VERIFY 75 of 75 modules; isolated 3 of 3.
- `CONTENT-DIFF SUMMARY: files 355, IDENTICAL 352, CHANGED 3, ADDED 0, REMOVED 0` against `KQSA62c3...`.
- 253,725,663 B (96.8%, 8,418,337 B spare). This equals AE~A's measured build at `ac5c378c1d`; no packaged input moved between
  the two commits.

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | CHANGED | `AMGT-ao-1` | as above (title case) |
| `lib/research/harvest/publication_gold.py` | CHANGED | COO~H `4d393e3521` + `fc5a0bf42d` | NONE through this function (see below) |
| `lib/research/harvest/finbert_sentiment.py` | CHANGED | COO~H `fc5a0bf42d` | NONE through this function (see below) |

**`publication_gold.py`:** the hunks delete `QUARANTINED_PUBLISHERS`, `GRADED_PUBLISHERS`, `is_quarantined` and
`_without_quarantined_jobs`. They remove the filter lines from `run_record_spans`, `publisher_coverage`, `daily_rows`,
`_iter_all_listing_hits`, `build_daily`, `_iter_latest_articles`, `build_mention` and `build_event`. All of these are builders.
No hunk touches the functions the routes call (`_day_of`, `_latest_gold_snapshot_rows_cached`, `BACKFILL_FLOOR`, `_baseline`,
`_event_id`, `GOLD_DAILY_TABLE`).

**`finbert_sentiment.py`:** the hunks remove the quarantine branch from `score_missing` and `_cmd_score`, plus one docstring in
`latest_scores`. The module is imported lazily inside `build_mention` only.

Any other changed file at build time is a STOP.

**EXPECTED OUTCOME, re-measured at `19cb3df089`:**

| check | base (deployed KQSA62c3) | after (local at `19cb3df089`) |
|---|---|---|
| r65 c17 | NO: 55 of 94 and 56 of 95 under the build commit's 36-acronym predicate (60 and 61 with no exception; row Z-S342) | YES |
| r64 c12 | YES | YES |
| r64 c9, c10, c11, c13, c14 | YES | YES |

The union of 5 suites is 1030 passed.

The blast radius, the rollback and WHAT THIS HALF DOES NOT COVER are unchanged. The act changes no collection.

**The instrument (row Z-S342, AE~A):** `r65_served.py --where deployed` reads `DISPLAY_NAME_ACRONYMS` from the LOCAL tree. So c17 on deployed is graded with the checkout AT THE BUILD COMMIT, where the local predicate equals the deployed one. Any other checkout grades deployed names with a foreign predicate.
