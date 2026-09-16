# U3-AC2 -- HAND-OFF: preserve-don't-clobber for seed_canonical_securities.py

**TO-U3-1 / cell `AT4-s-3` / `0.9.0_WK_POSN_ASTTAX~16` / re-cut @`8e67653049`.**
This is a DISCLOSURE AND HAND-OFF, not an edit.

## THE SURFACE AND ITS OWNER

| | |
|---|---|
| File | `data/black_diamond/scripts/classification/seed_canonical_securities.py` |
| Blob @HEAD | `fbbc7165d33198789d3a7788a557ed3f5ce75614` (296 lines, 15000 bytes) |
| **Owning lane** | **POD4 (DS-owned)** -- `.owned-paths.yaml:1712`, `"data/black_diamond/**": lane: POD4` |
| This worker's lane | POSN. `<paths>` grants the order file, this deliverables dir, the investigation channel. It does NOT grant the file above. |

**PLAINLY: POSN measured this and POSN does not own the fix. data/black_diamond/** is lane POD4 (DS-owned, .owned-paths.yaml:1712), so this worker RECORDED the change as a unified diff and applied nothing. The patch is handed to POD4 to apply, with the measurement and both controls attached.**

## THE PROPOSED CHANGE

`u3_proposed_patch.diff` (+57/-2 over the 296-line original), in this same
directory. It is a TRUE delta of the real bytes, not a sketch:

- `git apply --check` against the HEAD blob: **rc=0, applies cleanly**.
- NEGATIVE CONTROL: the same diff with one context line corrupted is
  **REFUSED**, so the check discriminates.
- Applying it reproduces, byte for byte, the exact file `U3-AC3` exercised.

## MECHANISM -- THE SIBLING'S, NOT A SECOND PATTERN

`infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-classifications.py`
`merge_item():72-120`: the module wins where it knows something; the TABLE wins
where the module holds only a placeholder; where BOTH know something and they
DISAGREE, nothing is decided there -- the disagreement is returned as a
**conflict for the caller to refuse on** (`:95`), with `--force` the only way
past it (`:159`, `:181`).

The patch reuses exactly that: a pre-read of the live row, per-field
disagreement collected as a conflict, the run **refusing with rc=1** rather than
writing, and `--force` as the single override. `is_placeholder()`'s half is
**inert** here -- this seeder never emits a placeholder, its `asset_class`
vocabulary being two hardcoded values.

## WHAT IT DOES NOT CHANGE

A FIRST MINT STILL MINTS: an absent row returns no conflict, so the 53 rows this seeder mints are minted identically pre- and post-patch (measured 53 = 53 in U3-AC3); the bd-securities limb, the dry-run path and every non-owned attribute are untouched.

## WHY IT IS NEEDED (measured, U3-AC1, scratch copy, live table never opened)

One re-seed reverts **4 of 4** carried five-class members present in this
seeder's list: `VXX`/`UVXY` `Structured`->`equity`, `QBER`
`Structured`->`fixed_income`, `PDBC` `Commodities`->`equity`. The seeder's
2-value vocabulary intersects the five ratified classes **0 of 5** -- it cannot
preserve a ratified class even by accident. FWD-5 ("defined in one place and it
flows") cannot hold while a routine re-seed silently reverts it.

## WHAT POD4 IS ASKED TO DO

Apply `u3_proposed_patch.diff` to the file above, under POD4's own lane and
commit gate. POSN has made no edit, staged nothing, and created no file under
`data/black_diamond/` -- verified `0` modifications against a matching
pathspec.
