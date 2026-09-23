# H03 step 1 -- adapter selection and call-site analysis

Author `0.7.0_AE_CloudOps~A`. Written against the H03 integration packet at pin
`fa65082078` (`org/tier1_exec/4.0.0_SA_CRO/deliverables/AMGT_R_CLOSER_20260923/H03_INTEGRATION_PACKET.md`),
the redacted replacement for revoked `84ba660442`. Measured on SITEZ at HEAD `eba69cac0b`.

NOTHING IS IMPLEMENTED, COMMITTED TO CODE, DEPLOYED OR CUT OVER BY THIS DOCUMENT. It answers
the packet's step 1 question -- WHICH adapter, at WHICH call sites -- because steps 2 and 3
(dependency closure, S3 prefix permissions) are both derived from that answer and neither can
be measured before it.

## 1. THE ADAPTER, NAMED

| what | where | vintage |
|---|---|---|
| gold count function | `lib/research/metrics/chatter_axis.py:387` `gold_daily_mention_scores` | HEAD `eba69cac0b` |
| the single read adapter beneath it | `lib/research/coverage/pool_reader.py:672` `gold_window_read` | same |
| the selector map | `lib/research/metrics/chatter_axis.py` `SOURCE_COUNT_FNS = {"legacy": default_daily_article_counts, "gold": gold_daily_mention_scores}` | same |
| the legacy incumbent | `chatter_axis.py:355` `default_daily_article_counts` | same |

`gold_daily_mention_scores` returns `{date: mention_score}` -- the tier-weighted graded figure --
where the legacy function returns `{date: article_count}`. Both fill `READ_DETAIL` in the same
shape, so a run's printed denominators read the same whichever source produced them. The gold
path opens NO second S3 client and NO second key layout: `test_one_adapter_for_both_reads`
asserts that, and the docstring at `:391` states it.

## 2. THE CALL SITES -- BOTH OF THEM, IN THIS LANE'S OWN FILE

`infra/aws/terraform/harvest/lambda_src/lambda_function.py`, this lane's file:

- `:54`  `compute_chatter_axis()` -- the pool-universe path
- `:65`  `compute_chatter_axis(universe_path=_UNIVERSE_SNAPSHOT_PATH)` -- the bundled-snapshot
  fallback, reached only when the pool read fails AND the repo fallback is absent

The packet says BOTH. Neither passes `count_fn` today, so both inherit
`chatter_axis.py:590`'s default `count_fn=default_daily_article_counts` -- the legacy source.
THE FALLBACK CALL SITE IS THE ONE THAT GETS MISSED: it is inside an exception handler, it is
the path that runs when the pool is already unhealthy, and a reviewer reading the happy path
never sees it.

## 3. THE FINDING THAT DECIDES THE SHAPE OF THE WORK

### 3a. A DENIED DAY STILL CARRIES A SCORE INTO THE SERIES

`pool_reader.py:689-693`, the gold adapter's own docstring, verbatim:

> A day graded PARTIAL or DENIED is counted in `states` (`partial`/`denied`) and STILL carries
> its `mention_score` in `counts` -- the state block, not a silent zero in the series, is what
> tells a caller the day was not a clean read; `complete` is False whenever either count is
> nonzero for the window

Confirmed at the bytes: `:710` `counts[day_str] = float(row.get("mention_score") or 0.0)` runs
for every in-window row regardless of `data_status`; `:711` `incomplete = sum(counters.values())`;
`:721` `"complete": incomplete == 0`.

CONSEQUENCE: a window of 29 DENIED + 1 PARTIAL days -- the exact population `1.0.0_SA_CTO~Z`
ruled on -- PRODUCES ROWS. It does not produce an empty series that would fall out naturally.

### 3b. AND ROWS DEFAULT STRAIGHT INTO THE FORBIDDEN STATE

`lib/research/metrics/generation_writer.py:269`:

    state = state or (STATE_COMPLETE if rows else STATE_EMPTY)

Coverage is never consulted here. So an uncovered-population run that passes no explicit state
lands on COMPLETE (rows exist) -- precisely what the ruling forbids. THE VIOLATION IS THE
DEFAULT, not a branch anyone wrote wrong. Silence selects it.

`GENERATION_STATES = (STATE_COMPLETE, STATE_EMPTY, STATE_FAILED)` at `:49`, and `:194` refuses
anything outside that tuple. So "neither COMPLETE nor EMPTY" has exactly ONE legal expression
today -- `STATE_FAILED` -- which is what the packet requires, what C-RANKING-GENERATION already
specifies, and why NO ENUM EDIT IS NEEDED. Consistent with CTO24857's withdrawal and with
"do not edit enum before L4-R". This lane will not touch the enum, and could not: all three of
`generation_writer.py`, `chatter_axis.py`, `chatter_gate.py` return VIOLATION lane=BASE_EXEC
for `0.7.0_AE_CloudOps~A` (3 of 3, rc=1).

### 3c. THE COVERAGE SIGNAL EXISTS -- BUT ONLY ON THE GOLD PATH

`gold_window_read` returns, per identity: `states` (`partial`/`denied` counters) and
`complete` (`incomplete == 0`), and `gold_daily_mention_scores:405-411` copies BOTH into
`READ_DETAIL[identity]`.

An earlier read of this seat's said the producer "cannot see coverage today". That is correct
for the LEGACY path and is exactly what step 1 fixes: wiring the gold adapter is what BRINGS the
`complete` / `states` signal into the producer. Stated precisely: the signal is absent today
because the legacy source is selected, not because the plumbing is missing.

### 3d. THE PUBLISH HAPPENS BEFORE THE HANDLER SEES ANYTHING

`chatter_axis.py:591` -- `write_fn: Optional[GenerationWriteFn] = default_write_generation`.
The default WRITES. `lambda_function.py` passes no `write_fn`, so by the time `handler()` holds
a summary the generation and pointer are ALREADY PUBLISHED.

A coverage check written in `handler()` is therefore POST-PUBLICATION. It would read correctly,
report correctly, and prevent nothing. This is the trap in this cell: the obvious place to put
the guard is the one place it cannot work.

## 4. THE DESIGN FORK THIS RAISES -- for `1.0.0_SA_CTO~Z` and `4.0.0_SA_CRO~Z`

The ruling is "must propagate through the existing FAILED route". The decision needs
`complete`/`states`, which only exist AFTER the read; the write happens inside the same call as
the read. This lane cannot edit the producer module. So the refusal must be expressed from
`lambda_function.py`, and there are exactly two shapes:

- **A. TWO-PHASE, lane-legal today.** Call `compute_chatter_axis(count_fn=..., write_fn=None)`
  -- the documented dry-run limb, which BUILDS every generation and pointer and writes nothing
  (`chatter_axis.py:597`) -- inspect `read_detail` for `complete`/`states`, then either write
  the built generation or write the FAILED marker. Needs no BASE_EXEC edit. COST: the handler
  now owns a publish decision the producer used to own, and the dry-run return contract becomes
  load-bearing for this lane.
- **B. A COVERAGE-AWARE STATE INSIDE THE PRODUCER.** Cleaner and belongs with the logic, but
  `chatter_axis.py` / `generation_writer.py` are BASE_EXEC: not this lane's to write, and it is
  a producer-semantics change, which is H's surface and plausibly L4-R territory.

RECOMMENDATION: **A**, because it is lane-legal, needs no ratified enum and no BASE_EXEC edit,
and leaves the producer's own semantics untouched for H's separate fetch-result-lineage work.
RECORDED AS AN ASSUMPTION, NOT A DECISION TAKEN: this seat has not written either and will not
cut code on this fork until `1.0.0_SA_CTO~Z` or the packet owner says which.

## 5. WHAT IS STILL UNMEASURED -- named so it is not mistaken for done

- The exact dependency closure for the gold path in Lambda (packet step 2). `gold_window_read`
  imports `lib.research.harvest.publication_gold.GOLD_DAILY_TABLE` at `:694` and calls
  `_gold_latest_snapshot_rows`; whether that closure pulls PyArrow in the REAL runtime is
  UNMEASURED here and the packet explicitly forbids expanding it by guesswork.
- The exact S3 prefixes the gold path reads (packet step 3). `gold_window_read` names
  `s3://<POOL_BUCKET> (gold/<GOLD_DAILY_TABLE>)` in its `store` field; the resolved values and
  the narrow permissions they imply are UNMEASURED.
- Whether the aggregate rule is per-identity or per-window. `complete` is PER IDENTITY; the
  producer ranks across many. What fraction of incomplete identities should fail a GENERATION is
  a CONTRACT question this lane must not invent.
- H's producer candidate `ac4316c447` is NOT accepted by this seat and is not evidence here.

## 6. PROVENANCE

Every figure above is `measured` at HEAD `eba69cac0b` on SITEZ unless the line says UNMEASURED.
Instruments: `comp-read --enumerate` (printed denominators: `chatter_axis.py` 924 lines /
31 sections; `generation_writer.py` 373 lines / 17 sections), `comp-find` unscoped
(`coverage_status` -> 72 hits across 70623 files scanned), `git cat-file`/`sed` at the cited
lines, and `owned-paths-validate.py --check-agent` WITH PATHS ON STDIN and a non-owned-path
negative control. Push state: LOCAL -- this device does not push.
