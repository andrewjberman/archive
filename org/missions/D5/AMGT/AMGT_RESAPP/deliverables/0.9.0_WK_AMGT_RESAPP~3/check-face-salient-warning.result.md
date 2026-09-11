# AMGT_RESAPP.TO-AMGT-rb-10 -- session log

**Worker:** `0.9.0_WK_AMGT_RESAPP~3` | **Worktree:** `/c/tmp/wk-amgt-2b-3`, branch
`wk-AMGT_RESAPP-2b-3`, cut from HEAD `3f2189f28b`. **Round 2b, FWD-10 continued** (fixes
C-S12, the CVO's FAIL on this same worker's own AMGT-r-10 round-2 attempt).

## THE BAR FIRST

`git rev-parse --abbrev-ref HEAD` -> `wk-AMGT_RESAPP-2b-3`; `test -d org && test -d .tools` ->
TREE-OK.

## THE DEFECT, RE-READ (C-S12)

AMGT-r-10 (this worker, round 2) fixed AMGT-s-10's AC6 by APPENDING a second trailing text tag:
`12345 [PROVISIONAL]` became `12345 [PROVISIONAL] [WARN]`. The CVO graded it FAIL (C-S12,
@b3acbcf3dd): "the rendered fixture changes 12345 [PROVISIONAL] to 12345 [PROVISIONAL] [WARN],
adding another plain suffix word to the same number-first presentation previously rejected ...
no rendered color, warning glyph, leading status, or equivalent change in visual prominence."
The token contract (green/OK, amber/WARN, red/BLOCKED) was sound and stays PRESERVED; only the
READING -- where the marker sits relative to the value -- was unfixed.

## (a) THE SALIENT RENDER

`lib/research/checkface/render_print.py`'s `render_value()`: for REFUSE and PROVISIONAL, the
marker icon now renders FIRST, before the value/reason text:
  - REFUSE:       `[BLOCKED] [REFUSED: <reason>]` (was `[REFUSED: <reason>] [BLOCKED]`)
  - PROVISIONAL:  `[WARN] <value> [PROVISIONAL]` (was `<value> [PROVISIONAL] [WARN]`)
  - PASS:         unchanged -- the bare value, no marker (deliberate: PASS's silence is part of
    what makes a marked row a genuine departure).
A check with no `marker` field (a pre-AMGT-r-10 row) renders exactly as it did before AMGT-r-10
(no leading or trailing icon) -- the icon stays additive, never required to avoid an
empty/blank render. `count in == count out` is untouched (no figure count logic was touched;
only the string layout of an existing render). No non-ASCII was introduced (AC4).

## (b) THE DIFFERENCE ARM, SAME NUMBER

New module `lib/research/checkface/salience_fixture.py`: `same_number_checks(value=12345)`
returns PASS/PROVISIONAL/REFUSE check rows that all carry the IDENTICAL `value` -- only
`verdict`, `reason` and `marker` vary. This directly answers C-S12's own complaint that
AMGT-r-10's round-2 test compared 500 vs 12345 (two different values), so string inequality
proved nothing about WHERE the marker sits.

New test `test_same_number_leads_with_marker_the_salience_arm` in
`lib/research/checkface/tests/test_checkface.py`: renders the fixture's three checks and
asserts PASS is the bare value (`pass_render == "12345"`, first char a digit), and PROVISIONAL
and REFUSE each LEAD with a non-digit status marker (`not render.strip()[0].isdigit()`).
Verified live:
```
PASS        -> '12345'
PROVISIONAL -> '[WARN] 12345 [PROVISIONAL]'
REFUSE      -> '[BLOCKED] [REFUSED: unit never confirmed against a field map]'
```
An existing test, `test_refuse_renders_marked_value_in_place_of_the_value`, asserted
`rendered.startswith("[REFUSED:")` -- true under the OLD trailing-icon layout but false now
that the marker leads. Updated it to assert `rendered.startswith(f"[{icon}]")` (derived from
the check's own marker, not a hardcoded literal) instead, preserving its original intent (the
render is never the bare value) while making it correct against the new leading-marker
contract.

## (c) THE SPEC SECTION

`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~3/SPEC_SECTION_checkface.md`
(this worker's own prior deliverable, superseding only the marker-PLACEMENT portion): s.0
records C-S12 and its fix; s.1's table now shows the LEADING format per verdict
(`[BLOCKED] [REFUSED: ...]` / `[WARN] <value> [PROVISIONAL]`) and states the marker's DATA face
and READING face must both place the icon ahead of the number, proven by the same-number
fixture; s.2's REFUSE-row description updated to "LEADING" instead of "appended"; s.4 states
the leading placement is what the eventual `.tsx` carries forward (whatever component/glyph it
uses for the marker renders BEFORE the value it modifies), and that a refused/provisional value
stays reachable but is never presented as trusted or read-first. Text only -- no `.tsx`, no
file under `portal/` (AC3).

## CONTROLS

**Mutant:** reverted `render_value()`'s REFUSE/PROVISIONAL branches to the OLD trailing-icon
layout (via a scratch backup, restored after), re-ran the suite. Predicted: the new salience
test fails (PROVISIONAL's render starts with the digit again), and the updated REFUSE test
(which now checks the marker leads) fails too; the three untouched tests keep passing.
Observed, ACTUALLY RUN: `2 failed, 3 passed in 0.13s` -- `test_refuse_renders_marked_value_...`
FAILED (`assert False`, `rendered.startswith(f"[{icon}]")` false under the reverted code) and
`test_same_number_leads_with_marker_the_salience_arm` FAILED
(`AssertionError: assert not True` -- `'1'.isdigit()` true, the reverted PROVISIONAL render
started with the digit again) -- matching the prediction exactly. Restored the file from the
scratch backup; `git diff --stat` after restore shows the same 23 insertions / 12 deletions as
before the mutant (the intended fix, unchanged); re-ran the suite: `5 passed`.

**Determinism:** `python -m pytest lib/research/checkface/tests -q` run twice back-to-back
after the restore: `5 passed` both times, identical summary line.

## THE BAR, RE-RUN CLEAN AFTER RESTORE

AC1 `5 passed in 0.04s` -- AC2 `prov_leads_marker True | pass_is_bare True | same_value_differs
True | ascii True` -- AC3 `0` -- AC4 `ascii True`. `git status --porcelain` shows only the
intended paths: `lib/research/checkface/render_print.py`,
`lib/research/checkface/tests/test_checkface.py`,
`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~3/SPEC_SECTION_checkface.md`
(modified), `lib/research/checkface/salience_fixture.py` (new).

## AC5 (judgment, never self-graded)

Recorded UNVERIFIABLE-BY-INSTRUMENT in the proof-of-spec instance; `status_reason` names
`3.0.0_SA_CVO~Z` as the oracle per G-14. Not graded here.

## DECLARED EXCLUSIONS

- Regenerating the three real landed `check_face_*.json` blocks (SAP_GY/BA_US/BABA_US Equity)
  with the new leading-marker render: those artifacts live under
  `0.9.0_WK_AMGT_RESAPP~8`'s deliverables/ subfolder, outside this worker's write surface and
  outside this cell's `WHAT TO PRODUCE` (`lib/research/checkface/` and this worker's own
  `deliverables/0.9.0_WK_AMGT_RESAPP~3/`). `render_print.py`'s `render_value()` is shared code:
  any future re-render of those three blocks picks up the leading-marker layout automatically,
  with no further code change.
- No `.tsx` / no `portal/` file (C-DESIGN-SPEC-FIRST, AC3).

## SURPRISES

None filed this cell -- every criterion was satisfiable as written within the declared write
surface; no path outside `<paths>` was needed.
