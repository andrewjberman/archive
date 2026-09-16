# AMGT-rj-13 -- SESSION LOG (0.9.0_WK_AMGT_RESAPP~22, 2026-09-15, site Z)

Worktree `C:/tmp/wk-amgt-11-5`, branch `wk-amgt_resapp-11-5`, fast-forwarded to `eff1b9f6ae`
(SITEZ after the drain of rj-8). Second and last order of chain E. The rj-8 log is
`SESSION_LOG.md` beside this one and is not touched.

## THE BAR, FIRST

`git rev-parse --abbrev-ref HEAD` -> `wk-amgt_resapp-11-5`; `org/` and `.tools/` present;
`lib/research/social/`, `lib/research/identity/`, the CRO brief and the account pass all
present. TREE-OK, no blocking row.

Premises re-grounded before any build or spend:
- `lib/research/social/measure.py` has no HTTP client (its `main` returns 4 on the word
  branch), `schema.json` + `validator.py` are the item contract. HOLDS.
- `comp-secrets list` carries the six Bright Data entries the issuer named. The key used is
  `brightdata-api-key`: it is the estate-wide key and the one that reaches the DATASETS
  surface (measure.py's F12 note). Verified live: `GET /datasets/list` -> 200, 1765 datasets
  (F12 measured 1763), and both `gd_lvz8ah06191smkebj4` ('Reddit- Posts') and
  `gd_lwxkxvnf1cynvib9co` ('X (formerly Twitter) - Posts') are in that listing. The SERP zone
  key was not read.
- Egress: `dfa63b6d92`, Andrew-direct ~05:42Z, "The whole sitez fabric has free egress this
  session".
- The one security: `BA_US_Equity` is 1 of 256 rows in the union universe
  (`~19/universe.v1.2026-09-15.json`, ticker 'BA US', name 'Boeing BA'), so the keywords are
  DERIVED from that row, not typed: 'Boeing' (label minus its trailing root) and 'BA'.
- The account pass holds Boeing as UNRESOLVED with value null -> the X second candidate has
  0 profile urls for this name. Row S3.
- `social/v1/` in the pool held 0 objects before this cell.

## WHAT WAS BUILT

`lib/research/social/collect.py`, `measurement.schema.json` (S-1, closed at every level),
`tests/test_collect.py` (29 tests, client stubbed), and one amended paragraph in
`__init__.py` (the package docstring said nothing here makes a network call; the one
non-ASCII glyph in that file is preserved, 1 before and 1 after).

ONE job, TWO keyword inputs, said plainly: company name and ticker root in a single job
(one trigger, one snapshot id), `num_of_posts` 25 each so the total cannot exceed 50, and
`limit_per_input` on the trigger query as a second vendor-side bound on the same number.

## FOUR THINGS THE VENDOR'S OWN DOCUMENTATION CHANGED, ALL BEFORE THE FIRST SPEND

1. **The `date` field is an enum.** My first constant read 'Last month'; the vendor's doc
   page lists `Past hour | Past day | Past week | Past month | Past year | All time`. Sent
   'Past month' and re-applied the 30-day window locally on each record's posted_at. Row S5.
2. **A genuine zero arrives as `status=failed`.** The monitor-progress doc lists 'No data
   found in discovery' and 'Snapshot is empty' among the failed error messages. A client
   that reads status alone records a zero as a FAILURE; those two messages map to
   ZERO_MATCHES here. Row S4.
3. **`canceled` is a status**, and is FAILED here.
4. **The trigger body is a bare array** (`TriggerInput: type: array`) -- already so.

## THE RUN

The literal AC2 invocation was run SEVEN times; the FIRST submitted the one job and every
later one resumed it from the ledger. No second discovery was ever sent.

| run | start (UTC) | JOB line | final vendor status | outcome |
| --- | --- | --- | --- | --- |
| 1 | 16:41:03 | `persisted-before-polling ... resumed=False` | running | STILL_RUNNING |
| 2-5 | 16:43:15 .. 16:49:40 | `RESUMED ... no new discovery submitted` | running | STILL_RUNNING |
| 6 | 16:52:45 | RESUMED | ready, 48 records | COMPLETE |
| 7 (graded) | 16:56:43 | RESUMED | ready, 48 records | COMPLETE, `state=COMPLETE` printed |

Between run 6 and run 7 three defects in my own output were fixed (commit `f7bc52f173`):
the POLL line printed the vendor's 'ready' but never the OUTCOME state; a resume of a
completed job would have recomputed latency as submission-to-now and grown on every
re-run (now pinned to the first observed completion, with a regression test); the COST
line cut the payload's key list. A verdict-only job log was added beside the ledger.

## THE NUMBERS (the finding row is S8)

- delivery: 48 records, 48 valid, 0 invalid, 0 errors; admitted 0, rejected_by_rule 22,
  provisional 26; stale 2, fresh 46; capped false at job level -- but the 'BA' input hit
  its own per-input limit (25 of 25), so that arm was truncated.
- quality: keyword 'BA' 25 -> REFUSE 22, PROVISIONAL 3, 22 distinct communities, mostly not
  Boeing (BritishAirways, degree and job boards); keyword 'Boeing' 23 -> PROVISIONAL 23, in
  plainly Boeing communities. No record can reach the item rule's PASS arm: the vendor
  record's 30 keys carry no per-post subject. Every author is UNRESOLVED.
- latency: 713.4 s recorded (submit -> retrieved); vendor `collection_duration` 709920 ms;
  ready between about 578 s and about 702 s after submission by the poll stamps.
- cost: NOT MEASURABLE with this key. No cost field on progress (running or ready) or on
  the snapshots listing, and `/customer/balance` refuses the key with 403. `cost.usd` is
  null with claim 'absent'; the held pre-call estimate was usd 0.075 against the usd 5 cap.
  Row S7.
- normalisation: 26 of 48 items carried non-ASCII, 137 characters removed; the served
  record is 0 non-ASCII bytes.

## CONTROLS

Mutants on the SERVED record against `measurement.schema.json`: positive control VALID; no
job id -> refused ('id' is a required property); state 'SUCCESS' -> refused; a smuggled
'feed' field -> refused; second_candidate 'RUN' -> refused; cap 51 -> refused.
Determinism: two resumed runs (write_pool False) produce identical documents minus
`generated_at`, and both equal the served record minus `generated_at`.

## ROWS FILED (all OBSERVATION, INERT)

S3 X candidate has 0 profile urls for Boeing; S4 vendor zero as status=failed; S5 date is an
enum; S6 the S-1 key has no security coordinate; S7 cost not measurable with this key; S8
the measurement itself.

## COMMITS (LOCAL, on `wk-amgt_resapp-11-5`)

- `5ac6e20930` the client, the S-1 schema, 28 stubbed tests.
- `f7bc52f173` the three output fixes, the job log, the `__init__` paragraph, rows S3-S7.
- this commit: row S8, the proof-of-spec instance, this log, the job ledger and job log,
  the measurement record copy, and the task order's `<status>` flip.

Nothing was pushed, merged, rebased or stashed. No feed, no schedule, no second security,
no X call, no SERP zone, no portal edit.
