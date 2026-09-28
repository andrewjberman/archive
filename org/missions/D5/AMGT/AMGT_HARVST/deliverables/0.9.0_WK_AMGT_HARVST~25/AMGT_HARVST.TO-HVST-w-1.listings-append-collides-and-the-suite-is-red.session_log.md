# Session log -- `0.9.0_WK_AMGT_HARVST~25` on `HVST-w-1` (re-issued, AMENDMENT 2)

`0.9.0_WK_AMGT_HARVST~23` cannot be resumed ("No transcript found for agent ID"). Its branch
`wk-hvst-w1-r8` carries commit `7c92bc5671` with the real repair to `uploads.py` and
`__main__.py`, its AC1 script, and its channel row. This worktree (`wk-hvst-w1-r8b`) branches
from that branch with AMENDMENT 1 (AC2's re-cut invocation) merged, per the order's Amendment 2.
**Nothing in `uploads.py` or `__main__.py` was re-derived or re-edited by this slot** -- both
files are inherited unchanged from `~23`'s commit. This slot's job was to re-run all three
criteria against the amended AC2 text and record ONE instance at ONE vintage.

## What was re-run, and why all three (not just AC2)

Per the order's Amendment 2: AC1 and AC3 are pure/local (a fake in-process s3 client; a `--help`
read) so re-running them costs seconds and keeps one instance carrying all three rows at one
vintage, rather than splitting one cell's proof across two folders at two vintages.

## AC1 (row `AMGT_HARVST-Z-W9-S1`, listings half)

Copied `~23`'s `scripts/ac1_listing_collision.py` verbatim into this slot's own scripts folder
(per the spawn instruction: the order's AC1 invocation names this `~25` path, so it is run from
here, not re-pathed). Ran it: negative control reproduces `PreconditionFailed` on the direct,
unwrapped `store.silver_append` call (HEAD's pre-fix listings shape); the repaired call site
(`uploads._silver_append_retrying_object_name`) lands both same-second appends at two distinct
object names (`part-20260927T120000Z.parquet` / `part-20260927T120000Z-r1.parquet`); row count
landed (2) equals the sum of both row sets. PASS.

## AC2 (row `AMGT_HARVST-Z-W21-S2` / `AMGT_HARVST-Z-W23-S1`)

Confirmed the order's AC2 `<invocation>` at HEAD (`0784a192d8`) reads, byte-for-byte:
`cd "$(git rev-parse --show-toplevel)" && python -m pytest lib/research/harvest/tests/ lib/opal_data_harvest/ -rA 2>&1 | tail -60`
-- the `/tests/` suffix dropped from the second path, exactly Amendment 1's text. Ran it
literally, twice (to check determinism of the environment-dependent case): **3 failed, 292
passed** both times. All three failing nodeids are pre-existing and outside this cell's
`<paths>` (neither `test_verification.py` nor `test_worker.py` is touched here):

- `test_verification.py::Tests::test_disabled_barrons_contract_defers_before_opening_a_browser`
  -- run 1: `KeyError: 'bundle'`; run 2: `FileExistsError: [WinError 183] Cannot create a file
  when that file already exists`. Same nodeid, two different causes across runs, matching the
  already-recorded finding (channel row, non-ASCII-free excerpt above line 1346 of
  `INVESTIGATION_v1.md`): this is a leftover-filesystem-state condition, not a logic defect
  introduced by this cell. Its assertion was NOT touched.
- `test_worker.py::Tests::test_single_broken_dow_jones_article_is_skipped_but_repeated_server_failure_stops`
  -- `SUBFAILED` twice per run, `AttributeError: 'NoneType' object has no attribute 'get'`, same
  in both runs. Pre-existing (same nodeid as row `Z-W21-S2`'s original measurement), outside
  this cell's write grant, assertion untouched.

BEFORE (already measured by the issuer, `lib/opal_data_harvest/` alone, row `Z-W21-S2`): 3
failed / 160 passed. AFTER (this slot's literal run of the AMENDED invocation, both named
directories): 3 failed / 292 passed (131 of the 292 from `lib/research/harvest/tests/`, all
passing, confirmed by a separate un-graded scoping read; 161 of 292 from
`lib/opal_data_harvest/`, one more than the 160 in the historical baseline -- an incidental
extra passing test added since that measurement, not chased). Same 3 pre-existing failures, no
regression, no new failure, no assertion weakened. Graded PASS: the invocation runs to
completion (no usage error), states both counts, names every failing test with its error text,
and the WinError-183-class case is reported with its cause per the order's own accepted-outcome
carve-out.

## AC3 (row `AMGT_HARVST-Z-S27`)

`--harvest-grammar` help text, OLD (pre-`~23`, `git show HEAD~1:lib/opal_data_harvest/__main__.py`
via the commit diff): `"run: turn on harvest-grammar bronze/silver writes (config key ...)"`.
NEW (current, inherited from `~23`): `"run: turn on the harvest-grammar bronze/silver row BUILD
(config key harvest_grammar) and build+pass a harvest_client to Worker so its harvest path is
reachable -- writes nothing to S3 by itself (HVST-h-10 ...)"`. No longer says "writes" for a
flag that writes nothing to S3. PASS.

## Controls

- **Mutant**: re-ran `~23`'s mutant independently in this worktree.
  `_silver_append_retrying_object_name`'s suffix line
  (`stamp_to_use = "%s-r%d" % (run_stamp, attempt)`) mutated to `stamp_to_use = run_stamp` (no
  suffix change on retry) -- AC1's script then raised
  `ClientError: PreconditionFailed ... exhausted object-name retries` (rc=1, was rc=0).
  Reverted via `git checkout HEAD -- lib/opal_data_harvest/uploads.py` (clean diff after);
  `py_compile` clean; re-run rc=0.
- **Determinism**: `ac1_listing_collision.py` run twice back-to-back post-revert; both runs'
  full stdout byte-identical, sha256 `db369c6be531d4a69c06d37904952f283e0d28dd56dbbebbdb4666d652d2f87a`
  both times -- the identical hash `~23` recorded, confirming the fix and script are unchanged
  across worktrees.

## Commit-gate

`.tools/commit-gate.sh` clean (py_compile + ds-precommit + ruff py39) on
`lib/opal_data_harvest/uploads.py`, `lib/opal_data_harvest/__main__.py` (both inherited,
untouched by this slot) and this slot's copy of
`org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~25/scripts/ac1_listing_collision.py`.
Zero non-ASCII bytes in the new script copy.

## Surprises

None new. `AMGT_HARVST-Z-W23-S1` (filed by `~23`, disarm owner `2.0.0_SA_COO~Y`) is the row this
slot's AC2 re-run answers; this slot did not edit that row (append-only, another serial's row).
No new off-mandate observation surfaced during this slot's re-runs.
