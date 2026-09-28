# Session log -- `0.9.0_WK_AMGT_HARVST~23` on `HVST-w-1`

## The three repairs

1. **AC1 (row `AMGT_HARVST-Z-W9-S1`, listings half).** `lib/opal_data_harvest/uploads.py`
   `HarvestUploader._run_listings` called `harvest_grammar.store.silver_append` directly, per
   listing, inside the loop -- neither retried nor grouped, unlike the articles path
   (`_run_articles`, which groups by `(source, run_stamp)` and calls
   `_silver_append_retrying_object_name`). Rewrote `_run_listings` to the same two-phase shape:
   a first pass builds bronze + rows and groups items by `(source, run_stamp)`; a second pass
   calls `_silver_append_retrying_object_name` ONCE PER GROUP with the group's concatenated
   rows, then fans the one receipt back out to every listing_id in the group for the db update
   and the `record()` event. `store.py` untouched. `max_attempts` untouched (default kept).
   No `sa`-special-casing: the fix is keyed on `(source, run_stamp)` alone.

2. **AC3 (row `AMGT_HARVST-Z-S27`).** `lib/opal_data_harvest/__main__.py`'s `--harvest-grammar`
   help string said "writes" for a flag that writes nothing to S3 by itself. New text: "turn on
   the harvest-grammar bronze/silver row BUILD ... writes nothing to S3 by itself".

3. **AC2.** The suite was already red at HEAD (row `AMGT_HARVST-Z-W21-S2`, 3 failed / 160
   passed on `lib/opal_data_harvest/` alone). This cell touches no test file and makes no
   attempt to turn the three red tests green -- they are outside this cell's write grant and
   are not this cell's defect. **AC2's own LITERAL invocation names a path,
   `lib/opal_data_harvest/tests/`, that has never existed** (only flat
   `lib/opal_data_harvest/test_*.py`) -- see surprise row `AMGT_HARVST-Z-W23-S1`. Run literally,
   per standing instruction (never re-path an invocation), it collects zero tests from either
   named directory (pytest rc=4, usage error), never reaching the counts the criterion's
   `<expect>` describes. Graded FAIL on that literal output. A DIAGNOSTIC-ONLY run (not the
   graded invocation) against the two REAL directories
   (`lib/research/harvest/tests/ lib/opal_data_harvest/ -rA`) shows `3 failed, 292 passed` --
   the SAME three pre-existing nodeids as `Z-W21-S2`, no new failure, no regression from this
   cell's own two production edits; the WinError 183 case is named with its cause and its
   assertion is untouched.

## Controls

- **Mutant**: `_silver_append_retrying_object_name`'s suffix line
  (`stamp_to_use = "%s-r%d" % (run_stamp, attempt)`) mutated to `stamp_to_use = run_stamp`
  (no suffix change on retry) -- AC1's own script then raised
  `ClientError: PreconditionFailed ... exhausted object-name retries` (rc=1), where it had been
  rc=0. Reverted; `py_compile` + a clean re-run (rc=0, identical byte-for-byte output) confirm
  the revert landed exactly the pre-mutant bytes.
- **Determinism**: `ac1_listing_collision.py` run twice back-to-back; both runs' full stdout
  are byte-identical (sha256 `db369c6be531d4a69c06d37904952f283e0d28dd56dbbebbdb4666d652d2f87a`
  both times).

## Commit-gate

`.tools/commit-gate.sh` clean (py_compile + ds-precommit + ruff py39) on all three touched
`.py` files: `lib/opal_data_harvest/uploads.py`, `lib/opal_data_harvest/__main__.py`,
`org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~23/scripts/ac1_listing_collision.py`.
Zero non-ASCII bytes in the new script (byte-delta detector).

## Surprise filed

`AMGT_HARVST-Z-W23-S1` (ARMED, disarm owner `2.0.0_SA_COO~Y`): AC2's invocation names a
never-existing path; disarm is a re-cut of the invocation (drop the `/tests/` suffix on the
second path), not a worker act.
