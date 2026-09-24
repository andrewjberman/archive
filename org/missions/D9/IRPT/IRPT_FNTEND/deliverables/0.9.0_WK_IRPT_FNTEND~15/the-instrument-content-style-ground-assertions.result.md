# IRPT_FNTEND.TO-FE-s-65 -- result (0.9.0_WK_IRPT_FNTEND~15)

These captures are FIXTURE-FED: the real `investor-reporting` route, served by this worktree's own
`vite` dev server, with every backend request answered at the network layer by
`scripts/ui-smoke.mjs`'s router (a declared `--fixtures` JSON map, or a forced `--fail`/`--delay`
hold) -- no live route, no live backend, was ever reached. That is the right evidence for THIS
card: FE-s-65 builds an INSTRUMENT (additive flags on `ui-smoke.mjs`) that every later round-11
visual cell depends on, and the instrument's own correctness is a property of its CODE and its
CONTROL ARMS (does an assertion actually distinguish a right state from a wrong one?), not of
whether any one route happened to be live when it was exercised. It is NOT the right evidence for
the other seven visual cells of this round, each of which DOES need FWD-12's real DONE WHEN
(familiarity on the real, wired page) and carries its own capture plan for that.

## Three passes
**Pass 1**: built the instrument, 17 of 18 criteria PASS, F65-AC16 REFUSED as written (measured:
the invocation's single `Export` click never reaches the submit control). Committed portal
`32fcfe12`, workspace `b54d015b53`. Drained by the issuer at workspace CLOUD `c71fad69a4`.

**Pass 2**: a coordinator message claimed F65-AC16's invocation had already been amended and
landed at CLOUD `c71fad69a4`. Verified independently before acting (`git diff`, `git show`, `git
rev-parse CLOUD`, the drain commit's own subject) -- the claim was FALSE at that commit: the edit
existed only on disk in the shared tree, never committed. Not executed on; filed as surprise row
`IRPT_FNTEND-W15-S2` instead. Fast-forwarded both repos as instructed (harmless, independently
verified as clean ancestors); committed the row at workspace `adefaece0e`. `<status>` left
`pending`, unchanged.

**Pass 3**: the coordinator confirmed pass 2's finding, apologized for the process error, and
landed the amendment genuinely at workspace CLOUD `6100a2fc06`. This worktree's HEAD (`adefaece0e`)
was NOT an ancestor of `6100a2fc06` (both `is-ancestor` checks returned false -- genuine
divergence from intervening commits, including another worker's own surprise row), so a real merge
was required instead of a fast-forward: one conflict, on the append-only investigation file, both
sides' rows kept as separate array entries (verified after resolution: 0 conflict markers, JSON
re-parses, 239 rows). Merge commit `73ea9594a5`. Read F65-AC16 fresh from this worktree's own
merged copy of the governing order (not the coordinator's paraphrase) before acting: it now carries
the amended invocation, second click included. Restarted the dev server, re-ran ONLY F65-AC16,
confirmed `DELAYED: api/scoped/investor-reporting/export (4000ms)`, stopped the server and
reverified the port closed. Re-recorded the proof instance (AC1-15/17/18 evidence reused verbatim;
only AC16's row, the three artifact pins, and the surprises array changed) and re-validated.

## Portal commit
`portal/scripts/ui-smoke.mjs` -- additive flags only: `--expect`, `--expect-text`,
`--expect-style`, `--expect-ground`, `--inject-css`, `--delay`, `--strict`. Old flags/lines
untouched (F65-AC2). New test surface: `src/pages/InvestorReporting/__tests__/fe-s-65/regression.sh`
and `.../fixtures/dead.json`. Committed at portal `32fcfe12` (pass 1), LOCAL on branch
`wk-irpt_fntend-11-65-fe-s-65-portal` (portal frozen), fast-forwarded to `71167fbf` in pass 2 (an
unrelated FE-s-73 test, not touching this cell's surface); not pushed.

## Workspace commits
Surprise row `IRPT_FNTEND-W15-S1` (pass 1, `b54d015b53`); surprise row `IRPT_FNTEND-W15-S2` +
fast-forward to `c71fad69a4` (pass 2, `adefaece0e`); merge to `6100a2fc06` resolving the
investigation-file conflict (pass 3, `73ea9594a5`); this proof-of-spec instance's AC16 update,
this result file, and the `<status>` flip (pass 3, final commit -- see WORKER REPORT for hash).
LOCAL on branch `wk-irpt_fntend-11-65-fe-s-65`, not pushed.

## Final measured state (this worktree, dev server port 5900)

- F65-AC1 (whole portal typechecks): `rc=0` -- **PASS**
- F65-AC2 (default behaviour unchanged, baseline @243089eb vs new, LOC/CANVAS/TEXT/REFAREAS):
  `REGRESSION: 4 of 4 default lines identical` -- **PASS**
- F65-AC3 (`--expect` PASS arm): `EXPECT[[data-slot="tabs"]]: PASS (1 visible)` -- **PASS**
- F65-AC4 (`--expect` FAIL arm): `EXPECT[[data-slot="no-such-slot-zzz"]]: FAIL (0 visible)` -- **PASS**
- F65-AC5 (`--expect-text` PASS arm): `EXPECT-TEXT[body::Investor Reporting]: PASS` -- **PASS**
- F65-AC6 (`--expect-text` FAIL arm): `EXPECT-TEXT[body::ZZZ NOT ON THIS PAGE ZZZ]: FAIL` -- **PASS**
- F65-AC7 (`--expect-style` PASS, `=`): `EXPECT-STYLE[body::background-color]: PASS rgb(244, 246, 250)` -- **PASS**
- F65-AC8 (`--expect-style` FAIL, `!=`): `EXPECT-STYLE[body::background-color]: FAIL rgb(244, 246, 250)` -- **PASS**
- F65-AC9 (`--expect-ground` PASS): `EXPECT-GROUND[body]: PASS rgb(244, 246, 250)` -- **PASS**
- F65-AC10 (wrong-ground control, after `--inject-css`): `EXPECT-GROUND[body]: FAIL rgb(196, 203, 219)` -- **PASS**
- F65-AC11 (honest summary count): `ASSERT-CONTENT: 2 of 4 met` -- **PASS**
- F65-AC12 (WIRE MATCH, live arm, `--click Export`): `FIXTURES-MATCH: matched 3 of 3` -- **PASS**
- F65-AC13 (WIRE MATCH, dead arm, authored `fixtures/dead.json`): `FIXTURES-MATCH: matched 0 of 1` -- **PASS**
- F65-AC14 (`--strict` fails): `EXIT=1` -- **PASS**
- F65-AC15 (`--strict` passes): `EXIT=0` -- **PASS**
- F65-AC16 (`--delay` PASS arm, AMENDED invocation with the second click): `DELAYED:
  api/scoped/investor-reporting/export (4000ms)` -- **PASS** (pass 3). Pass 1 measured this arm
  FAIL as originally written (single click; the toolbar `Export` control
  (`ExportButton.tsx:171-180`) only opens `ExportModal`, the POST fires from the modal's own
  `Create export` button, `ExportModal.tsx:257-266`) and REFUSED it rather than self-grading past
  it, filing surprise row `IRPT_FNTEND-W15-S1`; the `--delay`/`--click` instrument itself was
  verified sound at that time (an added second click, or a load-time URL with zero clicks, both
  printed DELAYED correctly). The issuer confirmed the same root cause and amended the invocation
  to `--click Export --click 'Create export' --delay ... --console DELAYED` (workspace CLOUD
  `6100a2fc06`, read fresh from this worktree's own merged copy, not the coordinator's paraphrase).
  Re-run against the amended invocation on a freshly restarted dev server: PASS, matching
  `<expect>` exactly.
- F65-AC17 (whole suite green, dev server stopped, port verified closed,
  `IRPT_FE_DEV_PORT` unset): `612 pass / 22 skip / 0 fail`, 2581 expect() calls, Ran 634 tests
  across 114 files. [56.41s] -- **PASS**
- F65-AC18: judgment, RECORDED, no verdict. The header comment above the flag-parsing block and
  the header comment above the expectation pass both cite THE INSTRUMENT grammar verbatim; every
  flag is repeatable via the file's own established `args.reduce` pattern; every PASS/FAIL/
  ASSERT/FIXTURES-MATCH/DELAYED line quoted above was produced by running the instrument, none
  hand-typed; F65-AC2's regression run is the old-flags/old-lines-untouched evidence.

## Mutant and determinism controls
- **Mutant**: the six built-in wrong-state arms (F65-AC4, AC6, AC8, AC10, AC13, AC14) each fired
  as expected -- every one printed its FAILING value, never silently reusing the passing arm's
  value. See the proof-of-spec instance's `controls.mutant` for the full comparison.
- **Determinism**: F65-AC3's own invocation run twice in immediate succession printed
  byte-identical deciding lines (`diff` rc=0). See `controls.determinism`.

All 17 mechanical criteria now measure PASS by their own printed output, with no FAIL row; F65-AC18
is RECORDED with no self-graded verdict. **`<status>` is flipped to `complete`** in this same pass,
per this order's own rule (flip only when VALID with no FAIL row).

## Rows filed
- `IRPT_FNTEND-W15-S1` -- OBSERVATION, INERT. Pass 1: named the exact mechanism (a second click on
  the modal's own submit control is needed) and the two diagnostic runs that isolated it from the
  instrument's own code. RESOLVED by the issuer's amendment at CLOUD `6100a2fc06`; F65-AC16 now
  reads PASS.
- `IRPT_FNTEND-W15-S2` -- OBSERVATION, INERT. Pass 2: a coordinator message claiming the amendment
  was already landed at CLOUD `c71fad69a4` was measured false at that commit before acting on it.
  Not a fault of this worker's process; the coordinator confirmed and corrected it in pass 3.

## Proof-of-spec
`org/missions/D9/IRPT/IRPT_FNTEND/deliverables/0.9.0_WK_IRPT_FNTEND~15/IRPT_FNTEND.TO-FE-s-65.the-instrument-content-style-ground-assertions.proof_of_spec.json`
-- `proof-of-spec-check.py` run before this file was finalized (pass 3, against the amended
governing order): `VALID (rc=0)`, 18 acceptance rows, 0 violations, invocation-alignment 17/17
match (confirming this instance's AC16 invocation now matches the amended order text exactly),
surprises-frame resolves both filed rows. No FAIL row remains -- `<status>` flip is correct.
