# complement-census.r17.result -- LGIC_ENFORCE.TO-EN-x-1-r17 (EN-x-1), 0.9.0_WK_LGIC_ENFORCE~1

**Built at commit `16184888d2` (the record), worktree `wk-lgic-enforce-17-1`, base `50b1aadf90` (cut from
round-17 issuance `c2181f8d7f`).**

## The cell

Finish the census round 16 could not reach: `FULL` (every `*.py` under any `fixed_inputs/` anywhere in
the LGIC tree) `MINUS PRIOR` (the paths round 16's census record actually carried). The domain is a
SUBTRACTION, never a project list and never the retired list -- round 15's forward list of two project
names is exactly how it lost 11 checkers.

## The pin, and how the population was re-derived

Pin: `50b1aadf909f7690e80c87ceadab607d295ab115` (this worktree's base, printed and carried in the record).
`FULL = git ls-tree -r --name-only <pin> -- org/missions/D14/LGIC/`, filtered to lines containing
`fixed_inputs/` and ending `.py` -- no project filter, no round filter, no filename-pattern filter: **37**.
`PRIOR = git show <pin>:.../RETIRED_BUT_RUNNABLE_R16.json`, the `path` values its `census.instruments[]`
actually carried, at the SAME pin: **23**. `COMPLEMENT = FULL - PRIOR` by path-string set subtraction: **14**.

**This is ONE HIGHER than the order's own framing control (13).** The control was measured at the
issuer's earlier `cut_pin` (`13566fbfe2`); my pin is this worktree's base (`50b1aadf90`, later), and
between those two commits the round-17 issuance itself minted `fixed_inputs/r17/check_en_r17.py` --
the checker now grading this very cell. That file is therefore IN my complement (it wasn't in the
issuer's), which is the SAME fourth-vintage-effect shape the order already names for
`LGIC_LGCTFM/fixed_inputs/r8/check_lt_r8.py`. Re-derived, not copied, per the order's own instruction;
disclosed rather than silently reconciled to 13.

## The three classes

| class | count |
|---|---|
| RETIRED-AND-DISCLOSED | 0 |
| RETIRED-BUT-SILENT | 0 |
| LIVE | 14 |

**Method, for every one of the 14** (the same method round 16's own record states it used): an unscoped
`comp-find` sweep of the member's owning project's surprise-channel (investigations/adjudications/
remediations) and decompositions, plus a name-glob for any `<PROJECT>_ROUND*_ANALYSIS.md` under
`org/tier1_exec/1.0.0_SA_CTO/deliverables/`, for `retir`/`superseded`/`falsif`/`vacuous`, cross-referenced
against every hit naming that member's own filename.

- **`LGIC_CANON`** (r1-r4, 4 members): DOC-band denominators 2/7/3/2 for the four terms; no hit names
  `check_canon_r1.py`, `check_canon_r2.py`, `check_canon_r3.py` or `check_cn_r4.py` -- the hits concern
  the PRD's exception clause, a v1 decomposition, a section-count remedy and a headline number, none a
  checker. No CTO round-analysis carrier exists for this project (name-glob: 0 of 1068 files).
- **`LGIC_NAMING`** (check_ln.py + r2-r5, 7 members): DOC-band denominators 12/1/2/3; no hit names any of
  the five genuine checkers. Round 5 ("`check_ln_r5.py` -- ... the CLOSING round") is the most recent
  round present, so nothing exists to retire it; its own `:213` "vacuous" hit is the checker's OWN
  self-test prose about a hypothetical failed arm, not a retiring record. No CTO round-analysis carrier
  exists for this project.
- **`LGIC_LGCTFM`** (r8/check_lt_r8.py, 1 member): DOC-band denominators 37/7/3/2, plus a direct 26-hit
  sweep on the literal string `check_lt_r8` -- every hit is an ordinary CMD reference, an acceptance-
  criterion record (its own round-8 task order records all three criteria PASS, rc=0), or an unrelated
  passage (a `retired_aliases` registry field, a different decomposition hazard). No retiring record.
- **`LGIC_ENFORCE`** (2 members): `g1_preimage/existing_alias.py` -- a 2-line DATA FIXTURE, not a checker
  (no CMD dispatch, no PASS/FAIL shape), excluded from round 16's own domain by its filter's construction,
  included here because this round's domain carries no filename filter; declared as a fixture per BOUNDS
  rather than dropped. `r17/check_en_r17.py` -- this round's own fixed input, the checker actively
  grading this cell right now; no round exists yet to retire it (same basis round 16 gave its own
  `r16/check_en_r16.py` entry).

**FIXTURES declared, not dropped, per BOUNDS** ("a fixture is not a checker, and that is a judgment you
must declare rather than make silently ... you may not drop one from the population"): `existing_alias.py`,
`r2/blind_seat.py` and `r3/blind_seat.py` (LGIC_NAMING's clean-context seat runners -- they print
`SEAT: OK`/`SEAT: ERROR`, not a subcommand-per-criterion verdict; each round's real checker re-derives the
prompt and re-parses the reply independently, per `blind_seat.py`'s own docstring). All three classed LIVE
(the schema admits no fourth value); the fixture judgment is stated in each entry's own `basis`.

**No `RETIRED-AND-DISCLOSED` and no `RETIRED-BUT-SILENT` this round** -- unlike round 16 (which found three
in the ENFORCE+LGCTFM domain it had already worked for fifteen rounds), the complement here is mostly
`LGIC_CANON` and `LGIC_NAMING`: two projects with no CTO round-analysis carrier at all yet, and one
(`LGIC_NAMING`) explicitly closed at round 5 with nothing after it to have retired an earlier round. The
absence of a RETIRED-BUT-SILENT finding is a MEASURED result of the same sweep that found three last round,
not a narrower sweep that stopped looking.

## Denominator re-read at completion

**37 -- NO DRIFT.** Re-run of the same `git ls-tree` filter at HEAD immediately before commit returned the
same 37; no sibling project's issuance minted or removed a `fixed_inputs/*.py` between this cell's pin and
its own completion.

## What this cell does and does not move

**Measures only.** No checker was touched -- every one censused is READ-ONLY (BOUNDS). No row was filed on
`LGIC_NAMING`, `LGIC_CANON` or `LGIC_LGCTFM`'s channels (read scope only, not write scope).

## Controls

**Mutant (FIRED-AS-EXPECTED, both), run against the committed record and the REAL `x1-census` arm, restored
byte-identical (`diff` clean, `git status --porcelain` clean against the committed blob):**
1. `how_enumerated` rewritten to `"walked the retired list of known retirements across the LGIC tree"` ->
   `FAIL-X1-CENSUS`, naming both "does not name fixed_inputs/ as the domain" and "enumerates FROM THE
   RETIRED LIST".
2. Last instrument entry (`LGIC_NAMING/fixed_inputs/r5/check_ln_r5.py`) dropped, `complement`/`live`
   decremented to 13 -> `FAIL-X1-CENSUS`, naming `complement says 13; the subtraction at that pin yields
   14` AND `NOT CLASSED (in the complement, absent from the record): [...check_ln_r5.py]` -- set equality
   caught the drop even though the printed arithmetic (13 = 13) was internally self-consistent, exactly the
   guarantee the checker's own docstring names.

**Determinism (STABLE):** `x1-census`, `r17-vintage-field` and `r17-stale-proofs` run twice in sequence
against the restored, committed record -- `cmp` reports the two capture files IDENTICAL, 3 `VERDICT:` lines
each run, same verdicts and `rc=0` both times.

## Mechanical result

`X1R17-AC1` PASS, `X1R17-AC2` PASS, `X1R17-AC3` PASS (guard-shaped: 1 commit since `cut_pin` `13566fbfe2`
-- the round-17 mint itself -- 0 proofs at risk, 0 named re-run, set equality holds). `X1R17-AC4` recorded
for `3.0.0_SA_CVO` at L9 with the bytes cited in the proof-of-spec instance, not asserted here.

## The cut-time bar, checked

"Can a CORRECT artifact FROM THIS CELL ALONE satisfy this criterion?" For AC1-AC3: yes, demonstrated by
this run (a correct record built from an honest re-derivation passes cleanly). For AC4: it is explicitly
routed to L9 and carries no verdict from this cell, which is the criterion's own design, not a defect of
it. No sixth instance of a cut-time-unsatisfiable criterion was found in this cell; none filed.
