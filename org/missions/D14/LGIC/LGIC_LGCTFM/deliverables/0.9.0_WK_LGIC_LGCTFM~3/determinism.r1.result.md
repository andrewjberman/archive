# LGIC_LGCTFM.TO-LT-d-1-r1 -- determinism result (round 1)

**Cell:** LT-d-1 (PRD T9, DEC-10). **Assignee:** `0.9.0_WK_LGIC_LGCTFM~3`.
**Commit:** `2deeff1764` on `wk-lgic-lgctfm-1-3` (LOCAL). Engine read at branch tip `9b628270a1` (LT-e-1/LT-e-2/LT-e-3 already merged there).

## What was built

`lib/tests/test_opal_lgctfm.py` (new, stdlib + pytest only). Two tests:

- `test_fork_grouping_is_exercised` -- sanity gate on the pinned input (below): both PLANE rows must
  land in the one FORK row the arms compare, or the arms below would compare nothing.
- `test_determinism_negative_then_positive_arm` -- runs the negative arm FIRST, then the positive arm,
  in that order inside one test function (so file-order/plugin reordering cannot invert the story).

## The pinned, fully-offline input

Two `forks` seed locations under a fictional bucket, both `:leaf` mode (`_seed_rows()`'s leaf branch adds
the seed prefix itself as one row and never shells out to `.tools/aws` -- `lib/opal_lgctfm.py:789-792`):

```
wk3-pinned-bucket:assets/bronze/:leaf
wk3-pinned-bucket:assets/bronze_legacy/:leaf
```

`twin_key()` collapses a `_legacy`-suffixed tier back to its base tier (`lib/opal_lgctfm.py:706-728`,
DEC-5 mechanism 2 -- "`_legacy` is not a tier"), so both prefixes reduce to the same twin key
(`assets/bronze/`) and the two resulting PLANE rows (`R-0001`, `R-0002`) are always grouped into exactly
one FORK row (`F-0001`, members `["R-0001","R-0002"]` when sorted -- the sort is exactly what is under
test). No AWS call, no registry-content dependency for the grouping itself (only `canonical_member`
selection touches the real `scopes.json`/`remediations.json`/ledger, which this suite does not assert on).

## Negative arm (fired first)

De-sorted copy, committed at
`org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~3/desorted/opal_lgctfm_desorted.py`
(never in `lib/`, never replacing the engine). One functional change from `lib/opal_lgctfm.py` at
`9b628270a1`: the `forks` verb's FORK-row grouping line

```
distinct = sorted(set(members))          # real engine
distinct = list(set(members))            # desorted copy
```

`lib/opal_lgctfm.py:878` builds the FORK row's own `"members"` list from this value directly (no other
sort touches it downstream, and `json.dump(..., sort_keys=True)` only orders dict KEYS, never list
elements) -- so removing the sort makes `"members"`' order a function of the process's string-hash order
(`PYTHONHASHSEED`, randomized per process by default), not of the input.

Two runs of the copy on the pinned input above, one per `PYTHONHASHSEED` value, each a fresh subprocess
(the seed is read once at interpreter start, so two calls inside one process could never discriminate
this): `PYTHONHASHSEED=0` and `PYTHONHASHSEED=1` are verified at this commit
(`PYTHONHASHSEED=<n> python -c "print(list({'R-0001','R-0002'}))"`) to iterate that exact two-string set
in opposite order --

```
PYTHONHASHSEED=0  ->  ['R-0002', 'R-0001']
PYTHONHASHSEED=1  ->  ['R-0001', 'R-0002']
```

-- a deliberate discriminator, not a flake left to chance on an unpinned seed. Measured on the committed
copy: the two runs' `contract.json` files differ at exactly the FORK row's `members` array (order
flipped), confirming the removed sort is load-bearing (the WORKER FACE's own fallback -- "remove another
and say which" -- was not needed).

## Positive arm (recorded after the negative)

Two runs of the real, unmodified engine (`lib/opal_lgctfm.py`) on the exact same pinned input, same two
`PYTHONHASHSEED` values: byte-identical `contract.json` files, both runs.

## DETERMINISM.json

`org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~3/DETERMINISM.json` --
`negative_arm.recorded_utc` = `2026-09-17T18:32:15.110194+00:00` (negative arm's own runs, `outputs_differ:
true`), `positive_arm.recorded_utc` = `2026-09-17T18:32:53.074093+00:00` (positive arm's own runs,
`identical: true`), the negative strictly earlier.

## Acceptance (post-commit re-run, worktree HEAD `2deeff1764`)

| id | subcommand | verdict |
|---|---|---|
| D1R1-AC1 | d1-pytest | PASS-D1-DETERMINISM-SUITE-PASSES (`2 passed in 2.28s`) |
| D1R1-AC2 | d1-negative-first | PASS-D1-NEGATIVE-ARM-FIRED-FIRST |
| D1R1-AC3 | judgment | UNVERIFIABLE-BY-INSTRUMENT, for `3.0.0_SA_CVO` at L9 |

## Declared exclusions

None. The removed sort was load-bearing on the first attempt; no second removal was needed.

## Notes for D1R1-AC3 (judgment, no verdict from this seat)

The removed sort (`lib/opal_lgctfm.py:878`, `forks` verb) is a real build site whose order reaches the
FORK row's own output field (`"members"`), on the engine's genuine `_legacy`-tier-collapse grouping path
(DEC-5 mechanism 2) -- not a stub bypassing the walk: the pinned `:leaf`-mode seeds are still fed through
`cmd_forks()`'s real `twin_key()`/grouping/`build_row()` machinery, the only thing skipped is the live S3
listing (`_seed_rows()`'s own leaf branch, by design, per its own docstring), which the grouping site under
test does not depend on.
