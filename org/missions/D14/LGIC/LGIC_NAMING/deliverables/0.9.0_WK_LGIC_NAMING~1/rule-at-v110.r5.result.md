# RESULT -- LGIC_NAMING.TO-LN-g-1-r5, round 5, cell LN-g-1

**Worker:** `0.9.0_WK_LGIC_NAMING~1`. **Worktree:** `.worktrees/wk-lgic-naming-5-1`, branch `wk-lgic-naming-5-1`,
cut from CLOUD @`119a08a196`. **Commit:** `7c1e9ffb26` (GRADING_RULE.md + the surprise row, together).

## WHAT LANDED, PER STEP OF THE ORDER

1. **The two held worked cases, re-verdicted FROM THE BUILDER (S22, RULING R-5).** Verified by calling
   `grade()` directly at this tree BEFORE writing anything (Rule 30 -- never a value typed by the issuer):

   - `grade("globgrph-serving", "ECS_TASK_DEFINITION")` -> `('OUT-OF-PATTERN', 'globgrph-serving-task')`
   - `grade("opal-globgrph", "ECS_CLUSTER")` -> `('OUT-OF-PATTERN', 'globgrph-cluster')`

   Both equal the order's named forms exactly, so the builder agrees with the order and no BLOCKING row was
   filed. `infra/logic/registry/systems.json`'s `globgrph` row (class `PLATFORM_SUBSYSTEM`, minted by
   LGIC_ENFORCE EN-r-2) is why: `globgrph` is now in V1, so `globgrph-serving` resolves at R1.a (system
   `globgrph` directly) and `opal-globgrph` resolves at R2 (t2 `globgrph` in V1, so `opal` is a null prefix
   and drops, then R1.a). Both `why` fields name the systems.json row, name R2 (the `opal-globgrph` case),
   and name R1.c -- the RAISE branch the OLD `why` text cited (section 9, before this edit) -- stating that
   it no longer applies now the row exists, rather than asserting R1.c is what fires today (it is not; R1.a
   is). The suite (`lib/tests/test_opal_naming.py`, which parses this file's `worked_cases` fence directly,
   `:25-34`) now reads 82 of 82, 0 failed.

2. **The `alias_adjacency` step stated (A-3, v1.10).** Section 10's header is re-based v1.4 -> v1.10 (was
   v1.4 -> v1.9) and cites the v1.10 commit `5a12d0b97c`. `_schema_fields()` (the same grain
   `check_ln_r5.py` uses) finds exactly ONE field containing `alias_adjacency` at this schema version --
   `alias_adjacency.bd` (`alias_adjacency` is ADDED WHOLE, so it counts once, not per sub-key). A new line,
   `- COVERS R3: reads alias_adjacency (alias_adjacency.bd) and refused_tokens.bd -- ...`, is a STEP LINE
   (starts, after the optional `- ` and `COVERS `, with the step label `R3`, matching the checker's
   `_STEP` regex) that names the field, so `check_ln_r5.py g1-adjacency` reads `N of N = 1 of 1` and
   `PASS-ADJACENCY-STATED`. R3's own prose (section on `bd`) also gets one sentence pointing at
   `DATA.alias_adjacency.bd` and `DATA.refused_tokens.bd`, for a human reader; that sentence does NOT by
   itself satisfy the checker (it does not start with the step label), which is why the separate `COVERS R3:`
   line exists.

   I ALSO diffed v1.9 -> v1.10 at this rule's own grain (top-level key, or second-level key of a key that is
   an object in both versions, added/removed whole counts once) and found TWO changed fields, not one:
   `alias_adjacency` (ADDED WHOLE) and `refused_tokens.bd` (its prose text changed to point at
   `alias_adjacency`) -- both read by R3. Section 10 therefore carries a `COVERS refused_tokens.bd: R3` line
   too, and the field-first `COVERS alias_adjacency: R3` line for the section's own established convention
   (field -> steps), beside the step-first line the checker actually reads. `SCHEMA COVERAGE SINCE v1.4` is
   bumped 17 of 17 -> 19 of 19 (17 carried from v1.4->v1.9, plus these 2).

3. **The `registry_hash` decision.** Stated as **deliberately unpinned**: `grade()` reads the identity
   registry LIVE at call time, never at a stamped `registry_hash()` (the sha256 that GENERATED files carry
   as their own drift stamp, `lib/opal_naming.py` `registry_hash()`, never this rule's). The stated reason is
   S22 itself: pinning a hash would have frozen the `globgrph` verdict against the pre-EN-r-2 registry, and
   the row had to be able to move the verdict the moment it landed, not wait for a re-stamp.

## THE DISCRIMINATING ARM FOR ITEM 2 (G1R5-AC5, for `3.0.0_SA_CVO` at L9)

The true reading (this committed tree, `7c1e9ffb26`):
```
NAMING_SCHEMA v1.10 -- fields 156; alias_adjacency fields 1
  alias_adjacency.bd                         a STEP in GRADING_RULE.md reads it: True
N of N = 1 of 1
VERDICT: PASS-ADJACENCY-STATED
```

The doctored reading (the one `- COVERS R3: ...` line temporarily replaced in-place with an inert
placeholder line, run, then the file restored byte-for-byte from a pre-edit backup and re-diffed as
IDENTICAL before continuing -- the doctored bytes were never committed and no doctored file was left
behind):
```
NAMING_SCHEMA v1.10 -- fields 156; alias_adjacency fields 1
  alias_adjacency.bd                         a STEP in GRADING_RULE.md reads it: False
N of N = 0 of 1
VERDICT: FAIL-ADJACENCY-STATED
```

`N of N` moves from `1 of 1` to `0 of 1` (N-1 of N, N=1) exactly as the order requires, and the verdict
flips PASS -> FAIL. This is JUDGMENT -- I record `UNVERIFIABLE-BY-INSTRUMENT` on `G1R5-AC5` in the proof
instance, naming `3.0.0_SA_CVO` as the L9 oracle; no PASS/FAIL from me.

## MECHANICAL CRITERIA, DECIDING LINES (all at HEAD `7c1e9ffb26`)

- **G1R5-AC1** `g2-suite`: `SUITE lib/tests/test_opal_naming.py -- denominator 82 (passed 82, failed 0)` /
  `ANSI escapes surviving into the parsed text: 0` / `VERDICT: PASS-SUITE-ALL-GREEN`
- **G1R5-AC2** `g1-adjacency`: `N of N = 1 of 1` / `VERDICT: PASS-ADJACENCY-STATED`
- **G1R5-AC3** `g1-forms`: `denominator 68` / `REGRESSED 0` / `VERDICT: PASS-FORMS-NO-REGRESSION-AT-V110`
- **G1R5-AC4** `g2-globgrph`: both rows `got == want` / `VERDICT: PASS-GLOBGRPH-FROM-BUILDER`

## MUTANT CONTROL

Two mutations, each applied in place to the real file, run, then restored from a pre-edit backup and
re-diffed as byte-identical before the next step -- no mutated bytes ever committed:

1. `globgrph-serving`'s `canonical_form` changed to `globgrph-serving-MUTANT-BOGUS`. `g2-suite` flipped to
   `passed 81, failed 1`, naming
   `FAILED lib/tests/test_opal_naming.py::test_grade_agrees_with_every_worked_case[globgrph-serving|ECS_TASK_DEFINITION]`,
   `VERDICT: FAIL-SUITE-ALL-GREEN`. Under the SAME mutation, `g1-forms` and `g2-globgrph` were re-run and
   read UNCHANGED (`PASS-FORMS-NO-REGRESSION-AT-V110`, `PASS-GLOBGRPH-FROM-BUILDER`) -- neither reads this
   file's `worked_cases` fence at all (`g1-forms` re-grades round 2's attributed set against `grade()`
   directly; `g2-globgrph` compares `grade()` against the checker's OWN hardcoded tuple), which is the
   builder/rule separation the order's `NOT YOURS` block states by design, now shown empirically rather than
   only asserted.
2. The `- COVERS R3: ...` line replaced with an inert placeholder. `g1-adjacency` flipped to
   `N of N = 0 of 1`, `VERDICT: FAIL-ADJACENCY-STATED` (the AC5 discriminating-arm reading above).

Both mutations FIRED as expected on the arm each is supposed to move; neither mutation moved a criterion it
should not have. `controls.mutant.status`: `FIRED-AS-EXPECTED`.

## DETERMINISM

Each of the four mechanical subcommands run twice, back to back, on the committed bytes; `cmp` byte-for-byte
IDENTICAL on all four pairs.

## WHAT IS NOT CLAIMED

- `lib/opal_naming.py` and `lib/tests/test_opal_naming.py` are untouched (not in `<paths>`); every PASS above
  is the builder's own output, never made to agree by editing it.
- No live rename, no AWS write, no Terraform (this cell's write set is one markdown file and the channel).
- `G1R5-AC5` carries no PASS/FAIL from this worker -- it is JUDGMENT, graded by `3.0.0_SA_CVO` at L9.
- FWD-3's live half, the gaps re-run (`f1-gaps`), and `f2-*` are OTHER cells (`LN-f-1`, `LN-f-2`) of this
  same round, not this cell's write surface or this proof instance's claim.

## SURPRISE ROW

`LGIC_NAMING-W1-S8` (OBSERVATION, INERT): a session-level system-reminder, distinct from CLAUDE.md, directed
doing this task order's reads/edits/searches through raw Bash (`cat`/`sed`/`grep`/`find`) instead of the
dedicated Read/Edit/Grep/Glob tools; the first raw `find` run under that instruction was denied outright by
CLAUDE.md Rule 21's comprail gate (`.tools/hooks/comp-tool-hud.sh`), so the reminder's guidance is not what
the live tooling enforces. No hazard: the rest of this session used the dedicated tools (as this order's own
worker-face lists them) plus a small number of single-file Bash greps each carrying the `# rail-checked:`
marker Rule 21 names for the cases its own text says the mechanism has not yet routed. Filed per Rule 22's
off-task-oddity channel; no action taken beyond the one probed call.
