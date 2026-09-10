# AMGT-s-12 -- session log

Worker `0.9.0_WK_AMGT_RESAPP~3`, task order `AMGT_RESAPP.TO-AMGT-s-12.identity-layer-the-root.md`,
worktree `wk-AMGT_RESAPP-1-3` cut from SITEZ @3dbada33de.

## Sequence

1. Tree check (`TREE-OK`), status flipped `staged` -> `pending` on the task order file.
2. Read the CRO's F6 method (`AMGT_RESAPP_LAMBDAS_PEERS_IRSCAN_20260910.md` s.2) and measured the live
   corpus directly (openpyxl, `data_only=True`, read-only) rather than trusting the brief's numbers:
   89 folders, 49 with a one-pager workbook, 54 total `*ONE PAGER*.xlsx` files (5 folders carry two).
3. Wrote `lib/research/identity/resolver.py` -- `make_cell`, `infer_sa_symbol`, `resolve`,
   `render_together`. No network call, no vendor host (AC4 checked directly).
4. Wrote `lib/research/identity/self_test.py`, exercising the REFUSE/ADMIT difference arm on the same
   record (AC1) -- PASS on first correct run.
5. Wrote `lib/research/identity/build_universe.py`; first pass measured 47/49 one-pager folders MEASURED
   after a strict ticker-shape regex rejected `WALMEX* MM` (the `*` convention). Widened the regex to
   accept `*` (documented in the script); re-ran: 48 MEASURED, 41 UNRESOLVED, 89 of 89 (AC2). The
   remaining UNRESOLVED-with-workbook case (Rio Tinto) was inspected directly and found to be genuinely
   broken template residue (`HESAY-US EQUITY`, `#N/A Invalid Security`) -- left UNRESOLVED rather than
   guessed.
6. Wrote `f6_remeasure.py` per the cell's own stated method (CSC sheet, fixed 12-name KPN set, not the
   CRO's undefined "SAP sheet" -- no sheet named `SAP` was found on any workbook read). Result: 48
   stale / 4 own / 2 no-CSC of 54, an exact match to the brief's CITED 48/4/2 (AC3).
7. AC5 checked directly against `universe.json`: `sa_symbol`/`ir_domain`/`social_account` MEASURED == 0
   for all 89 entries.
8. Committed the module + deliverables at `074d0d1ebeb31631e871e60b24f84fcd70edae0b`. Ran a determinism
   control (two full re-runs of both scripts, timestamps masked: byte-identical) and a mutant control
   (a scratch copy of `resolver.py` with the UNRESOLVED-refusal branch disabled: the mutated
   `render_together` no longer refuses, and `self_test`'s own assertion catches it -- `AssertionError:
   render_together must REFUSE on an UNRESOLVED dependency`, rc 1). Restored `universe.json` /
   `f6_remeasure.json` to the committed bytes via `git show HEAD:<path> > <path>` after each re-run
   (never `git checkout --`, per this worker's git-safety bound).
9. Filed `AMGT_RESAPP-Z-W3-S1` (OBSERVATION, INERT): the cell text names "that folder's
   `*ONE PAGER*.xlsx` workbook" singular, but 5 of 89 folders carry two, and at least one pair
   (Imperial Brands) disagrees materially (one stale copy, one real analyst set). Non-blocking --
   `universe.json`'s tie-break (first file that yields a MEASURED ticker, all matching filenames
   recorded) did not affect any criterion; `f6_remeasure.py`'s own population is workbooks, not
   folders, and is unaffected.

## What is NOT done (declared, not hidden)

- The numeric `sa_id` and the live SA fetch path: AMGT-s-b4's, out of lane (Andrew-direct @d09e26e1b1;
  `1.0.0_SA_CTO~Z` msg 21056).
- `ir_domain` / `social_account`: UNRESOLVED everywhere, by design (bound d) -- no SERP zone request, no
  social lookup, no vendor call made or attempted.
- Nothing under the OneDrive corpus was written to; nothing was copied out beyond the measurements in
  `universe.json` / `f6_remeasure.json`.
