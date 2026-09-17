# LGIC_ENFORCE.TO-EN-p-4-r3 -- placement result

**Worker:** `0.9.0_WK_LGIC_ENFORCE~6`. **Order:** `LGIC_ENFORCE.TO-EN-p-4-r3` (`EN-p-4`, round 3).

## What was done

1. **Move (item 1).** All 18 files sitting directly under `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/`
   with no serial folder were `git mv`'d to the destination the issuer's fixed
   `.../fixed_inputs/r3/PLACEMENT_MAP.json` names for each -- its first minting author's folder, measured by
   the issuer with `git log --diff-filter=A` before the move. The map was not recomputed. Committed
   `b595cc87500bf5cc95e3100a75c741efee2fa6c6` (18 renames, 0 content changes).

2. **Live readers re-pointed (item 2).** The 4 string literals in 3 files the order named:
   - `0.9.0_WK_LGIC_ENFORCE~3/instrument/census.py:19` (`OUT = ...`) -- now points at
     `deliverables/0.9.0_WK_LGIC_ENFORCE~3/TF_LABEL_CENSUS.md`.
   - `0.9.0_WK_LGIC_ENFORCE~3/controls/t2_coverage.py:55` (`open(...)`) -- same destination.
   - `2.0.0_SA_COO~G/tools/issuance_rulings.py`'s `selftest()` fixture: the `led` ledger text and the `ff`
     variable now cite `deliverables/0.9.0_WK_LGIC_ENFORCE~1/FIRM_FORMS_READERS.md`; the `newf` CONTAINS-case
     variable, which illustrated "a NEW sibling in the ruled directory" using `LIMB_ROOTS_CENSUS.md` at the
     cut, now uses a fictional sibling of `ff`'s new directory (`NEW_SIBLING_FIXTURE.md`) because the move put
     `LIMB_ROOTS_CENSUS.md` under a *different* author folder (`~3/`) than `FIRM_FORMS_READERS.md` (`~1/`), so
     it no longer shares `ff`'s directory. `python issuance_rulings.py --selftest` still reports `SELFTEST: PASS`
     after the repoint (all 6 self-checks true).
   Committed `55913196125eed7e4b0e93349b1980d96a6f449a` (see COMMITS in the worker report).

3. **FIRM_FORMS_READERS census re-derived, pinned (item 3).** The held 62-entry edit does not exist (reverted;
   its re-apply script lived only in a session scratchpad). The relocated
   `deliverables/0.9.0_WK_LGIC_ENFORCE~1/FIRM_FORMS_READERS.md` now carries ONE fenced json:
   `{"vintage": "b595cc87500bf5cc95e3100a75c741efee2fa6c6", "exclusions": [...], "files": [...]}`.
   `git grep -l firm_forms <that vintage>` names **84** tracked files; one declared exclusion (the issuer's own
   `deliverables/2.0.0_SA_COO~G/fixed_inputs/` directory -- `check_en_r2.py` and `check_en_r3.py`, where the
   token is only the census's own default search string, never a schema read) removes **2**, leaving **82
   listed**, each with a `class`. **S21's disarm**: the two LGIC_NAMING records LN-g-1-r4's worker wrote
   (`deliverables/0.9.0_WK_LGIC_NAMING~3/LGIC_NAMING.TO-LN-g-1-r4.grading-rule.proof_of_spec.json` and
   `.../grading-rule.r4.result.md`) are listed `another-project`. The pinned vintage is this order's OWN move
   commit -- the checker recomputes the grep itself, so a record written after that vintage (including this
   result file and this order's own proof instance) does not move it.

4. **S35's count (item 4).** RULING/row `LGIC_ENFORCE-S35` records 17 ownerless deliverables; the true figure
   at the cut was **18** -- all 18 blobs first-commit at or before the vintage S35 itself was surfaced at
   (2026-09-16 07:29 -0400, preceding S35's 14:20Z `surfaced_at`), per the issuer's PLACEMENT_MAP.json
   `note_on_s35`. This cell moved all 18; S35 undercounted by one rather than the population having grown.
   This is a context correction the issuer's fixed input already carries; no row is filed by this worker for
   it (RULINGS numbers in the order are context, and item 4 asks only that this be stated in the result
   record).

## Verification (re-run at HEAD `55913196125eed7e4b0e93349b1980d96a6f449a` in this worktree, the checker's own vintages)

- `check_en_r3.py p4-population` -> `PASS-P4-POPULATION-EMPTY` (18 at the cut, 0 remain)
- `check_en_r3.py p4-destinations` -> `PASS-P4-DESTINATIONS-ALL-PLACED` (18 of 18 present)
- `check_en_r3.py p4-citations` -> `PASS-P4-LIVE-READERS-REPOINTED` (6421 .py files scanned, 18 old paths, 0 hits)
- `check_en_r3.py p4-readers-census .../0.9.0_WK_LGIC_ENFORCE~1/FIRM_FORMS_READERS.md` ->
  `PASS-P4-READERS-CENSUS-EQUALS-VINTAGE` (84 grepped, 1 exclusion rule -> 82 expected, 82 listed)

## Not done, and why not

- **P4R3-AC5** is a judgment criterion, graded by `3.0.0_SA_CVO` at L9 on whether each row's class is right and
  whether the two S21 rows read `another-project`. Recorded `UNVERIFIABLE-BY-INSTRUMENT` in the proof instance,
  naming `3.0.0_SA_CVO`.
- No record citing an old flat path was rewritten (task orders, proof instances, surprise rows, ledger entries,
  logs -- history pinned at its vintage; most may not be edited by anyone). Only the 4 live-reader literals in
  code and the FIRM_FORMS_READERS.md content itself (the file this order's own item 3 names) were touched.
