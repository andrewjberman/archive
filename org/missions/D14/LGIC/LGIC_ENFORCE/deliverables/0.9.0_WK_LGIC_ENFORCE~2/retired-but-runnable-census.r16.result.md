# retired-but-runnable-census.r16.result -- LGIC_ENFORCE.TO-EN-s-1-r16 (EN-s-1), 0.9.0_WK_LGIC_ENFORCE~2

**Built at commit `d01cf4af0e` (the record), worktree `wk-lgic-enforce-16-2`, cut from round-16 issuance
`14d80144dd`.**

## The cell

Census every `fixed_inputs/` checker across LGIC_ENFORCE and LGIC_LGCTFM -- enumerate the CHECKERS first
(never the known-retirement list), then ask of each whether a retiring record exists and whether the
instrument itself discloses it.

## The denominator, and how it was enumerated

`git ls-tree -r --name-only HEAD -- <LGIC_ENFORCE fixed_inputs> <LGIC_LGCTFM fixed_inputs>` at HEAD
`938ea238ed`, filtered to paths matching `/check_(en|lt)[_a-z0-9]*\.py$`: **16 LGIC_ENFORCE + 7
LGIC_LGCTFM = 23**. Cross-checked by two independent per-project counts that agreed.

## The three classes

| class | count |
|---|---|
| RETIRED-AND-DISCLOSED | 0 |
| RETIRED-BUT-SILENT | 3 |
| LIVE | 20 |

**Every RETIRED-BUT-SILENT instrument, by path, and how its silence was determined:**

1. **`check_en_r13.py`** -- the one already known. Round 15's discriminator sweep
   (`DISCRIMINATOR_SWEEP_R15.json`, result table rows 1-3) marks CMDs `p37-population`, `p37-tokens` and
   `p37-producers` RETIRED; the round-15 CTO analysis and CVO L9 `@c6ac61b33a` both adopt RETIRED over
   RE-POINT. **Measured in THIS worktree at 2026-09-19T15:16:42Z**: `fixed_inputs/r13/` holds only
   `R13_BASE.json` and `check_en_r13.py` -- no `RETIRED.md`, and the checker's own docstring/output carry
   no retirement notice. The sibling cell `EN-m-2` (`0.9.0_WK_LGIC_ENFORCE~1`) is adding a `RETIRED.md`
   into this same directory on its own branch concurrently; this reflects what my checkout showed, not
   that cell's result.
2. **`check_en_r11.py`** -- `LGIC_ENFORCE-S90` (surfaced by `3.0.0_SA_CVO`, GROUNDED): `core_stale`'s bar
   at `:172`, `ok = rec.get(...) == n and len(listed) > 0`, is FALSIFIED -- it forces a real-but-never-
   at-risk path to PASS. Confirmed still at those exact bytes at HEAD. The round-12 decomposition
   (`LGIC_ENFORCE_DECOMP.md` s.0l.4 item 5, s.0l.5) and the round-12 task order's own BOUNDS both state
   this checker is CLOSED and not edited, and that **"a census before the next cut"** -- this cell -- is
   owed instead of a repair. No comment, docstring line, or output string anywhere in the file names S90
   or the falsification.
3. **`check_lt_r1.py`** -- `LGIC_LGCTFM-S18` (GRADUATED disposition, `hazard_standing` still ARMED at
   read time): `base_ref()`'s two remaining callers, `x2_flag_untouched` (`:1508`) and `x3_opened_filed`
   (`:1567`), PASS on an EMPTY window -- a vacuous PASS, reproduced by both the original filer and
   `3.0.0_SA_CVO`'s own adjudication read. The remedy is explicit: **"NOT a repair ... editing a frozen
   graded input would move no grade while falsifying a record (R-43) ... the act belongs to whichever
   round next touches that checker."** No disclosure anywhere in the file.

## Named and deliberately excluded

**`check_en_r2.py`** (`LGIC_ENFORCE-S55`): its RULING RED limb (`r3_tests`/`r4_tests`/`r5_tests`) is
LIVE-blind against a red base -- its ANSI strip carries no `\x1b` and parses zero named failures. GRADUATED
disposition, `hazard_standing` still ARMED. Kept **LIVE**, not RETIRED-BUT-SILENT: the remedy names an
in-place edit still intended (`\x1b` added to the strip pattern), and no record disposes its CMDs' PASS
as retired or moot the way r11/r13/lt-r1's records do. The distinction is stated in the entry's own
`basis` field rather than silently folded into either verdict.

## The 20 LIVE checkers

LGIC_ENFORCE (13 of its 16, the other 3 being `r11`/`r13` above): `check_en.py`, `check_en_r2.py` through
`check_en_r10.py`, `check_en_r12.py`, `check_en_r14.py` through `check_en_r16.py`. LGIC_LGCTFM (all 6 of
its 7, the other 1 being `r1` above): `check_lt_r2.py` through `check_lt_r7.py`. See the record's own
`instruments` array for the full per-file basis; every LIVE entry states the same unscoped sweep found no
retirement/falsification hit naming that file, with `check_lt_r4.py` noted specifically as the SIBLING
COPY OF `check_en_r11.py`'s bar that WAS repaired (S90's own carrier census names it fixed, not retired).

## What this cell does and does not move

**Measures only.** No checker was touched -- every one censused is READ-ONLY (BOUNDS). No row was filed
on LGIC_LGCTFM's channel (read scope only, not write scope). The remedy for the three RETIRED-BUT-SILENT
instruments is the CTO's to decide on this measurement, not this cell's.

## Controls

**Mutant (FIRED-AS-EXPECTED, both):** (1) `how_enumerated` rewritten to describe walking the retired list
-> `s1-census` FAILs naming the domain violation. (2) `check_en_r13.py`'s `instrument_discloses_it`
flipped to `true` while its class stayed `RETIRED-BUT-SILENT` -> `s1-census` FAILs naming the
class/disclosure contradiction. Both restored byte-identical against a `.scratch/` backup (`diff` clean,
`git status --porcelain` clean against the committed blob).

**Determinism (STABLE):** `s1-census`, `r16-vintage-field` and `r16-stale-proofs` run twice in sequence
against the restored, committed record -- identical output and `rc=0` both times.

## Mechanical result

`S1R16-AC1` PASS, `S1R16-AC2` PASS, `S1R16-AC3` PASS (guard-shaped: 1 commit since `cut_pin`
`808ef7f397` -- the mint itself -- 0 proofs at risk). `S1R16-AC4` recorded for `3.0.0_SA_CVO` at L9 with
the bytes cited in the proof-of-spec instance, not asserted here.
