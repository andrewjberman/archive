# Session log -- `0.9.0_WK_AMGT_HARVST~26` on `HVST-x-1`

**Read in full before acting:** the task order's worker face, and
`org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_Y/WHY_THE_RED_TESTS_ARE_STILL_RED_20260928.md` (@`9a5d538d35`).

## Item 1 -- the `.json()` guard (`lib/opal_data_harvest/publishers.py:672`, `DowJones.check`)

Guarded the `.json()` call: `.json()` returning a non-dict (including `None`) or raising a decode
error now raises `AuthExpired("Dow Jones session is logged out")`, the same exception every
`check()` caller already handles, instead of `AttributeError` on a live auth path. `check()`'s
CONTRACT is unchanged for every input that already worked (a valid logged-in or logged-out JSON
body behaves exactly as before).

Proved directly (never through the suite) by
`org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~26/scripts/ac1_json_guard.py`,
which pulls the PRE-FIX `check()` body verbatim from git pin `402a3414c7c8ae9a7ea9eb69c2209fef7a740ed8`
(the commit at the start of this cell) rather than retyping it, to guarantee the negative control
reproduces the exact defect rather than an approximation of it.

## Item 2 -- the test-double gap (`lib/opal_data_harvest/test_worker.py`)

`test_single_broken_dow_jones_article_is_skipped_but_repeated_server_failure_stops` previously
patched the WHOLE `DowJones` class with `patch("lib.opal_data_harvest.publishers.DowJones",
return_value=remote)` and set `client.session = None`. Traced the live `AttributeError` and found
the patch never took effect: pytest's rootdir-based import (no `lib/__init__.py`) loads this test
as `opal_data_harvest.test_worker`, so the code under test resolves `DowJones` off the
`opal_data_harvest.publishers` module object, while the string-targeted `patch()` imports and
mutates a DIFFERENT module object, `lib.opal_data_harvest.publishers` (pythonpath `.` makes that
import succeed silently). The mock never touched the object actually used, so the REAL, unguarded
`check()` ran against `session=None` and raised. Filed as a surprise row (see below) rather than
investigated further, since the task's own diagnosis independently named the double as
incomplete and prescribed the shape of its completion.

Completed the double in the shape `test_bronze_capture.py:285`/`:296` and
`test_retrieval_provenance.py:239` use: `client.session` is now a small stub answering
`/client?legacy=false` with a valid logged-in body, and only `DowJones.discover`/`DowJones.article`
are replaced, via `patch.object(DowJones, ...)` on the class object imported directly by this test
file (so there is no string-target/module-identity mismatch). `check()` now runs FOR REAL and
unmocked in this test. `DowJones.check()`'s contract was not bent to fit the double.

## Item 3 -- the barrons quarantine (`lib/opal_data_harvest/test_verification.py`)

Added `@unittest.skip(...)` to
`test_disabled_barrons_contract_defers_before_opening_a_browser`, reason text naming the
alternation (`KeyError: 'bundle'` / `FileExistsError: [WinError 183]` across identical runs, no
intervening edit) and that its diagnosis belongs to cell `w-4`. No assertion in the test body was
touched.

## The three criteria (literal invocations, no `&&`, no pipe, no redirect)

- **AC1** `python org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~26/scripts/ac1_json_guard.py`
  -> rc=0, PASS. (a) pre-fix `check()` (from the git pin) raises `AttributeError: 'NoneType' object
  has no attribute 'get'`; (b) the same input through the current `check()` raises
  `AuthExpired: Dow Jones session is logged out`; (c1) a valid logged-in body still passes with no
  exception; (c2) a logged-out body still raises `AuthExpired`.
- **AC2** `python -m pytest lib/research/harvest/tests/ lib/opal_data_harvest/ -rA --tb=line` ->
  `306 passed, 1 skipped in 3.23s`, 0 failed (BEFORE: `3 failed, 306 passed`). Passed count did not
  fall (306 -> 306); the quarantine's reason is printed in the `-rA` summary.
- **AC3** `python -m pytest lib/opal_data_harvest/test_verification.py -rA --tb=line` ->
  `3 passed, 1 skipped in 0.08s`, 0 failed (BEFORE: `1 failed, 3 passed`). The skip reason string is
  printed verbatim, naming the alternation and cell `w-4`.

## Controls

- **Mutant** (on the item-1 guard): reverted `check()` to the pre-fix unguarded body, re-ran AC1's
  script -> rc=1, `(b) ... AttributeError ... FAIL: expected AuthExpired`, `AC1 FAIL`. Reverted the
  mutation back to the guarded version (`git diff --stat` confirmed the restored file matches the
  intended edit: 11 insertions, 3 deletions against HEAD); re-ran AC1 -> rc=0, PASS again.
  `.tools/commit-gate.sh` and `ruff` re-run clean after restoration.
- **Determinism**: AC1's script run twice back-to-back post-restore, stdout byte-identical both
  times, sha256 `56399fc9fb87c0a8cbd67f3933bf5dd141e7bf7f8b5ad2261b22232e9a89c4a4`, rc=0 both runs.

## Commit gate

`bash .tools/commit-gate.sh` (py_compile + ds-precommit + ruff py39) clean for all 4 touched `.py`
files: `lib/opal_data_harvest/publishers.py`, `lib/opal_data_harvest/test_worker.py`,
`lib/opal_data_harvest/test_verification.py`, and this cell's `scripts/ac1_json_guard.py`.

## Surprise row filed

One row, `AMGT_HARVST-Z-W26-S1`, ARMED, `disarm_owner: 2.0.0_SA_COO~Y`: the module-identity
mismatch behind item 2's `AttributeError` (`patch("lib.opal_data_harvest....")` targets a DIFFERENT
module object than the one pytest's rootdir-based import actually uses for `lib/opal_data_harvest`
test files, because `lib/__init__.py` does not exist while `lib/opal_data_harvest/__init__.py`
does) is a GENERAL pattern, not specific to this one test. The sibling occurrence at
`test_worker.py:51` (`patch("lib.opal_data_harvest.transport.time.time", ...)`) currently still
"works" only because it patches an attribute of the shared stdlib `time` module (a singleton),
not because the patch target is sound -- a future patch of the same `"lib.opal_data_harvest...."`
shape against a non-singleton target would silently no-op exactly as item 2's did. Not
investigated further or repaired beyond this cell's own two lines (bounds: three mechanical
criteria, no fourth; this is off-mandate).
