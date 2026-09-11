# AMGT_RESAPP.TO-AMGT-r-10 -- session log

**Worker:** `0.9.0_WK_AMGT_RESAPP~3` | **Worktree:** `C:/tmp/wk-amgt-2-3`, branch `wk-AMGT_RESAPP-2-3`,
cut by hand from `SITEZ` @`3730474e77`. **Round 2, FWD-10** (fixes AMGT-s-10's AC6 FAIL).

## THE BAR FIRST

`git rev-parse --abbrev-ref HEAD` -> `wk-AMGT_RESAPP-2-3`; `test -d org && test -d .tools` -> TREE-OK.
TO status flipped `staged -> pending` as the first act (this instance's own commit `c5516e28b53b6086d328233b1e178f5a6f063371`).

## THE DEFECT, RE-READ

AMGT-s-10's own AC6 (judgment, graded by `3.0.0_SA_CVO~Z`) FAILED: `'12345 [PROVISIONAL]'` skims,
on a fast read, as "a number, fine" -- the held-back verdict lived in `check_face.json`'s `verdict`
field (the DATA) and was too easy to miss in `render_print.py`'s bracket-text-only rendering (the
READING). AMGT-s-10's own SPEC_SECTION_checkface.md s.4 explicitly deferred the colour/icon choice
to a later cell -- this cell.

## THE MARKER (a)

`lib/research/checkface/markers.py` (new): `MARKERS = {PASS: (green, OK), PROVISIONAL: (amber,
WARN), REFUSE: (red, BLOCKED)}`. Two guards run AT IMPORT TIME, not merely documented:
1. **MECE by subtraction** (Rule 24 postulate i): `MARKERS`'s keys are diffed against
   `lib.research.rules.VERDICTS` both ways -- a verdict the rule can return but this module has no
   entry for, or an entry naming a verdict outside the rule's domain, raises `ValueError`.
2. **Distinctness**: the three `(colour_token, icon)` pairs are diffed for duplicates -- two
   verdicts sharing a marker raises `ValueError` before the module can even be imported.

`run_checks.check_one()` attaches `marker_for(verdict.verdict)` to every check row it returns; no
change to `check_block()`'s count semantics (C-MARK-NOT-DEGRADE unaffected: 5 figures in, 5 checks
out, same as AMGT-s-10 measured).

`render_print.render_value()` appends the marker's `icon` beside a REFUSE or PROVISIONAL render:
`'[REFUSED: <reason>] [BLOCKED]'`, `'<value> [PROVISIONAL] [WARN]'`. PASS renders bare (no marker
text) -- deliberately: leaving PASS unmarked is itself part of what makes a REFUSE/PROVISIONAL row
register as a genuine departure on a fast scan, and it is also what keeps AMGT-s-10's original three
tests passing byte-for-byte (`render_value(measured_check) == "999"`, unchanged).

## THE DIFFERENCE, EXERCISED (b)

A fourth test, `test_marker_distinct_per_verdict_the_reading_arm`
(`lib/research/checkface/tests/test_checkface.py`), builds a PASS, a PROVISIONAL (via a
`currency_caveat`, same shape as BABA_US_Equity's real finding) and a REFUSE (via an `INFERRED`
unit) figure from `check_one()`, and asserts pairwise distinctness at BOTH grains: the DATA face
(`marker.colour_token`/`marker.icon`) and the READING (`render_value()`'s output). Run:
`python -m pytest lib/research/checkface/tests -q` -> `4 passed` (AMGT-s-10's original 3, unchanged,
plus this one).

The fixture from AMGT-s-10 (`lib/research/checkface/fixtures.py`'s `FIXTURE_BLOCK`, unmodified: a
PASS name field, a PASS revenue figure, a REFUSE on an INFERRED unit, a REFUSE on an UNRESOLVED
sign, a PROVISIONAL on a `currency_caveat`) was re-run through the now-marker-bearing
`run_checks.run_raw_block()` and written fresh to this worker's own deliverables:
`check_face_fixture.json` / `.md`. Count in 5, count out 5 (C-MARK-NOT-DEGRADE held). 5 of 5 checks
carry a marker; 3 distinct `(colour_token, icon)` pairs across the 3 verdicts present; PROVISIONAL
and REFUSE both marked. The rendered `.md` shows
`12345 [PROVISIONAL] [WARN]` for the PROVISIONAL row and
`[REFUSED: ...] [BLOCKED]` for both REFUSE rows -- visibly distinct from the two PASS rows'
bare `Fixture Co` / `500`.

## THE SPEC SECTION (c)

`SPEC_SECTION_checkface.md` (this worker's own copy under `deliverables/0.9.0_WK_AMGT_RESAPP~3/`,
superseding the marker portion of AMGT-s-10's original section of the same name -- that section's
data-face/print-path/count-preservation contract is unchanged and not repeated here beyond what
context requires). Names `green`/`OK`, `amber`/`WARN`, `red`/`BLOCKED` as the tokens the `.tsx`
binds; states that a refused/provisional value stays reachable (in the JSON, on hover/expand in the
eventual page) but is never presented as trusted; states explicitly that PASS renders unmarked on
the print path by design. No layout, pixel or component chosen -- C-DESIGN-SPEC-FIRST holds.

## CONTROLS, BOTH ACTUALLY RUN

**Mutant (two, for full disclosure):**
1. `markers.py`'s `PROVISIONAL` entry mutated to collide onto `PASS`'s (`green`/`OK`). This did
   NOT reach the test suite at all -- the module's own import-time distinctness guard raised
   `ValueError` during test COLLECTION (`1 error`), one layer earlier than the predicted test
   failure. Reverted; `git diff` on `markers.py` empty (byte-identical), `4 passed` restored.
2. A second mutant, bypassing that guard without touching `markers.py`: `run_checks.check_one()`
   hard-coded to relabel a PROVISIONAL verdict's marker as PASS's marker. This reproduced the
   originally-predicted shape exactly: `1 failed, 3 passed` -- ONLY the new difference-arm test
   (`test_marker_distinct_per_verdict_the_reading_arm`) failed (`assert ('green', 'OK') !=
   ('green', 'OK')`); the original three tests were unaffected, confirming the new test -- and only
   the new test -- is what catches this exact defect shape. Reverted; `git diff` on `run_checks.py`
   empty (byte-identical), `4 passed` restored.

**Determinism:** `check_face_fixture.json` regenerated a second time from the same
`FIXTURE_BLOCK` (a pure function over a static dict), written to `.scratch/` and diffed
byte-for-byte against the committed copy -- empty. Two back-to-back `pytest` runs both report
`4 passed`.

## DECLARED EXCLUSIONS

- The `.tsx` page render: C-DESIGN-SPEC-FIRST; AC3 refuses a `.tsx` and this cell's own BOUNDS
  name the same refusal explicitly.
- Regenerating the three REAL landed blocks' `check_face_*.json` (SAP_GY/BA_US/BABA_US, under
  `0.9.0_WK_AMGT_RESAPP~8`'s deliverables) with markers: those files are AMGT-s-10's own landed
  deliverable and READ-ONLY to this cell (this cell's WHAT TO PRODUCE names
  `lib/research/checkface/` and this worker's OWN `deliverables/` subfolder, not another
  worker's). The shared `run_checks.check_one()` code path now attaches a marker to ANY block run
  through it (real or fixture) -- proven on the fixture per (b) -- so a future re-run of those
  three blocks would carry markers automatically; this cell did not re-run them because doing so
  would write into a path outside its granted surface.
- A print-path marker glyph on PASS rows: a deliberate DESIGN CHOICE (see s.1/(a) above), not an
  incompleteness -- PASS staying unmarked is part of the mechanism, not a gap in it.

## SURPRISE FILED

`AMGT_RESAPP-Z-W3-S5` (OBSERVATION, hazard_standing ARMED, disarm_owner `2.0.0_SA_COO~ZZZ`): the
repo's root `.gitignore` line 47 (`lib/`, generic Python-boilerplate) blankets the ENTIRE `lib/`
tree, including the already-tracked `lib/research/checkface/` this cell writes to. A brand-new file
there (`markers.py`) was invisible to a plain `git status`/`git add` (no `??` line at all) until
diagnosed with `git check-ignore -v`. Not blocking THIS cell (`.tools/safe-commit.sh` already
force-adds its declared pathspec, confirmed: `markers.py` landed in commit `c5516e28b5`), but ARMED
for any future new file under `lib/research/` read by a plain git-status sanity check instead of the
sanctioned wrapper.

## COMMITS

1. `c5516e28b53b6086d328233b1e178f5a6f063371` -- the work: `markers.py` (new), `run_checks.py`,
   `render_print.py`, `tests/test_checkface.py`; this worker's `SPEC_SECTION_checkface.md`,
   `check_face_fixture.json`, `check_face_fixture.md`; the surprise-channel row; the TO file's
   `staged -> pending` flip.
2. This instance's own commit: the `proof_of_spec.json`, this `result.md`, and the TO file's
   `pending -> complete` flip.
