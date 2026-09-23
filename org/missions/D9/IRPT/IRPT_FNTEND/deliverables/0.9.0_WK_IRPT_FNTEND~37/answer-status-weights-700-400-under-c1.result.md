# IRPT_FNTEND.TO-FE-s-87 -- result (0.9.0_WK_IRPT_FNTEND~37)

These captures are FIXTURE-FED: the real `investor-reporting` route, served by this worktree's own
`vite` dev server (port 6003, this worker's own block 6000-6004), with every backend request answered
at the network layer by the fixture router (`scripts/ui-smoke.mjs`'s own mechanism) -- no live route,
no live backend, was ever reached.

## Read first (HOW step 1)

`portal/DESIGN.md` C1-C12 in full (C1: "Lato ... at two weights only: 400 ... and 700 ... No 300, 500,
600 or 900"), `portal/CLAUDE.md` in full, the PRD's FWD-12 ENDPOINT/CONTRACTS text (v0.10 @4bc62712f2),
the CTO's round-13 analysis (`CTO_ROUND_ANALYSIS_IRPT_FNTEND_ROUND_13_20260922.md`), and
`REMEDIATION_v10.md` (the round-14 slug: FE-s-87 closes the residual FE-s-84 left OPEN -- `AnswerStatus.tsx`
still measured `font-semibold`/`font-medium`, weights 600/500, neither legal under C1). Also read
`REMEDIATION_v10.md:5`'s own disclosure of this round's baseline suite state: "648 pass / 27 skip / 2
fail. The two failures are committed sibling fixtures missing unprojected_grant" -- a pre-existing,
already-known, out-of-grant residual on cell FE-s-81's surface (`__tests__/fe-s-13/gen-corpus.ts`'s
generated `fe-s-13-wire.json`/`fe-s-14-print-v1.json`), confirmed again below at F87-AC7.

## Fix -- AnswerStatus.tsx weight classes (the whole grant)

`AnswerStatus.tsx:84`: `font-semibold` (600) -> `font-bold` (700), the state-label badge
(`data-slot="answer-state"`, the text `labelForState` returns -- "Ready", "Partial", etc.). `:88`:
`font-medium` (500) -> `font-normal` (400), the qualifier badge (`data-slot="answer-qualifier"`, shown
only when `complete` is false). No other line in this file touched -- confirmed by `git diff --stat`:
1 file changed, 2 insertions(+), 2 deletions(-). No test anywhere in the suite pins the old
`font-semibold`/`font-medium` classes on either selector (checked: `comp-find 'font-semibold|font-medium'`
and `comp-find 'answer-state|answer-qualifier'` over `__tests__/` -- the only `font-semibold` hits are
`fe-s-3/dropdown-class.test.ts`, unrelated, and `MethodAndSources.tsx`, a different file outside this
cell's grant; the `answer-state`/`answer-qualifier` hits are `fe-s-30`/`fe-s-32`'s driver scripts, which
read TEXT only, never weight), so no sibling test needed updating.

Read both weight-bearing PNGs myself: `f87_ready_state_700.png` (complete/"Ready" state) shows the
"Ready" label visibly bold, no qualifier badge present (complete state), white panel, `#C4CBDB` hairline
border. `f87_qualifier_400_and_state_700.png` (qualified/"Partial" state) shows "Partial" visibly bold
beside "Qualified answer -- not a complete report" at a clearly lighter weight, on the same capture --
the two co-located labels are visually and measurably distinct, not accidentally equal.

## Acceptance

- **F87-AC1** (whole portal typechecks): `$ tsc -b --noEmit` / `rc=0` -- **PASS**
- **F87-AC2** (READY fixture: state-label reads "Ready" AND measures weight 700 -- WIRE MATCH + NAMED
  CONTENT, controls a+b): `EXPECT-TEXT[[data-slot="answer-state"]::Ready]: PASS`,
  `EXPECT-STYLE[[data-slot="answer-state"]::font-weight]: PASS 700`, `ASSERT-CONTENT: 1 of 1 met`,
  `ASSERT-STYLE: 1 of 1 met`, `FIXTURES-MATCH: matched 3 of 3`, `KEY-VALIDITY: 3 of 3 valid consumed.ts
  operation keys` -- **PASS**. PNG read confirms bold "Ready" label, no qualifier badge.
- **F87-AC3** (WRONG-STATE NEGATIVE CONTROL, control c: the same "Ready" text assertion against the
  qualified/"Partial" fixture): `EXPECT-TEXT[[data-slot="answer-state"]::Ready]: FAIL`,
  `ASSERT-CONTENT: 0 of 1 met` -- **PASS**. Genuinely discriminates: the qualified fixture's real state
  label is "Partial", confirmed by PNG read.
- **F87-AC4** (qualified fixture: qualifier badge carries its text AND measures 400, co-located state
  label still measures 700): `EXPECT-TEXT[[data-slot="answer-qualifier"]::Qualified answer]: PASS`,
  `EXPECT-STYLE[[data-slot="answer-qualifier"]::font-weight]: PASS 400`,
  `EXPECT-STYLE[[data-slot="answer-state"]::font-weight]: PASS 700`, `ASSERT-CONTENT: 1 of 1 met`,
  `ASSERT-STYLE: 2 of 2 met` -- **PASS**. PNG read confirms the visible weight contrast on the same
  capture.
- **F87-AC5** (GROUND ON THE ACTUAL CONTAINER, control d) -- **PASS, on the COO's amended invocation.**
  The original single invocation paired `--expect-ground` with `--inject-css` in ONE call, which was
  structurally impossible: `scripts/ui-smoke.mjs:437-442` applies every `--inject-css` unconditionally
  BEFORE the `--expect-ground` measurement loop at `:557-574` (flag order on the command line does not
  matter -- both arg lists are extracted by an order-independent `reduce()` over the whole `args` array,
  `:145-146`), so a single capture could never print both a pre-inject PASS and a post-inject FAIL. This
  was filed as row `IRPT_FNTEND-W37-S1` (BLOCKING, disarm_owner `2.0.0_SA_COO~F`) and reported, not
  self-graded past. **COO AMENDMENT** split the criterion into two separate `node scripts/ui-smoke.mjs`
  calls in one shell command: first capture (`f87_ground_positive.png`, no injection) --
  `EXPECT-GROUND[[data-slot="answer-status"]]: PASS rgb(255, 255, 255)`, `ASSERT-GROUND: 1 of 1 met`;
  second capture (`f87_ground_wrong.png`, injected `#c4cbdb`) --
  `EXPECT-GROUND[[data-slot="answer-status"]]: FAIL rgb(196, 203, 219)`, `ASSERT-GROUND: 0 of 1 met`.
  Both match the amended `<expect>` exactly: the container genuinely grounds white (C3's panel role)
  absent injection, and the wrong-ground control genuinely discriminates (FAIL, never a vacuous PASS).
  Re-run live by this worker on the amended text (2026-09-22, port 6003) -- matches the issuing COO's own
  independent pre-amendment re-run exactly. Row `IRPT_FNTEND-W37-S1` DISARMED per the amendment's own
  stated condition.
- **F87-AC6** (ABSENT-SELECTOR CONTROL, control e: qualifier badge genuinely absent on the
  answer-BEARING/complete=true fixture): `EXPECT-STYLE[[data-slot="answer-qualifier"]::font-weight]:
  UNMEASURABLE (selector matched nothing)`, `ASSERT-STYLE: 0 of 1 met` -- **PASS** (matches
  `<expect>UNMEASURABLE</expect>`; rc=1 per the script's own FE-s-74 fail-closed-on-unmeasurable design,
  unrelated to the text match). PNG read confirms the qualifier badge does not render on the complete
  state.
- **F87-AC7** (whole suite green, excluding the disclosed cross-cell fixture gap) -- **PASS, on the
  COO's amendment-2 corrected invocation.** The literal `bun test src/pages/InvestorReporting` invocation
  genuinely reads 2 fail in every round-14 worker's isolated worktree, because none of the four cells'
  worktrees can see the others' fixes until the drain: `648 pass`, `27 skip`, `2 fail`,
  `2704 expect() calls`, `Ran 677 tests across 127 files` -- exactly the residual `REMEDIATION_v10.md:5`
  names at cut time. Both failures are in
  `__tests__/fe-s-81/generator-output-carries-unprojected-grant.test.ts`, exercising `FE-s-85`'s own cell
  (row `W25-S1`), whose regenerated fixtures are committed on ITS OWN branch only -- not a regression on
  this cell's surface (`git diff --stat` confirms this worker's ONLY change is `AnswerStatus.tsx`, 2
  lines). This worker's own first-pass filter (`grep "^✗" .suite_check_87.log | grep -vc
  "generator-output-carries-unprojected-grant"`, amendment 1) was itself reported and later found broken
  by the issuing COO in two independent ways: (a) `NO_COLOR=1` does not suppress bun's ANSI codes here,
  so a bare `grep "^✗"` matched ZERO lines regardless of real failures -- `UNEXPECTED-FAIL-COUNT=0`
  printed UNCONDITIONALLY, a vacuous pass (first caught by worker `~36`'s row `W36-S2`); (b) the exclusion
  pattern used the hyphenated test-FILE name, which never matched the actual printed line text (spaced,
  the `describe`/`test` block's own wording), so even post-ANSI-strip the exclusion matched nothing.
  **COO AMENDMENT 2** corrects the filter: strip ANSI first (`sed -r 's/\x1b\[[0-9;]*m//g'`), then exclude
  on the stable criterion-id token `F81-AC3/AC4` (present in both known lines, absent from every other
  line). Re-run live by this worker on the amended text (2026-09-22, dev server stopped first -- `curl`
  confirmed port 6003 closed `000`, `IRPT_FE_DEV_PORT` unset): the cleaned log's raw `grep "^✗"` count is
  exactly **2** (positive control -- the filter genuinely finds failures now, unlike amendment 1's silent
  zero), both lines are `✗ F81-AC3/AC4 -- generator output carries unprojected_grant on every entry,
  every file > fe-s-13-wire.json` and `... > fe-s-14-print-v1.json`, both excluded by the `F81-AC3/AC4`
  token, `UNEXPECTED-FAIL-COUNT=0`. Matches the issuing COO's own independently re-verified corrected
  invocation exactly, and matches worker `~36`'s own row `W36-S2` disclosure. Row `IRPT_FNTEND-W37-S1`
  (and `W36-S2` where filed) DISARM per amendment 2's own stated condition; the true
  whole-suite-including-FE-s-85 bar is verified separately by the COO at drain time in the merged tree.
- **F87-AC8** (judgment, graded by the CVO at L9): RECORDED, no verdict taken. State-label weight
  measured 700, qualifier weight measured 400 on the same co-located capture (F87-AC4); the wrong-state
  control (F87-AC3) and absent-selector control (F87-AC6) both genuinely discriminate, confirmed above;
  the ground measurement targets `[data-slot="answer-status"]`, the actual panel container (C3's role),
  not the page canvas -- confirmed white pre-inject and genuinely discriminating post-inject (F87-AC5, on
  the COO's amended two-capture invocation).

## Controls (THE CRITERION RULE / C-S176, five controls)

- (a) WIRE MATCH -- F87-AC2's `FIXTURES-MATCH: matched 3 of 3`, `KEY-VALIDITY: 3 of 3` (every capture).
- (b) NAMED CONTENT -- F87-AC2 ("Ready", weight 700) and F87-AC4 (qualifier text + weight 400,
  co-located state weight 700).
- (c) WRONG-STATE NEGATIVE CONTROL -- F87-AC3, discriminates (0 of 1 met).
- (d) GROUND ON THE ACTUAL CONTAINER -- F87-AC5, on the COO's amended two-capture invocation: first
  capture PASS white (no injection), second capture FAIL on injection -- genuinely discriminates.
- (e) ABSENT-SELECTOR CONTROL -- F87-AC6, discriminates (UNMEASURABLE, not a vacuous PASS).

**DECLARED-KEY VALIDITY vs EXERCISED FULFILMENT, stated separately per C-S176 step 6:** all 8
`<expected_criteria>` keys parse in this instance (DECLARED-KEY VALIDITY: 8 of 8). EXERCISED
FULFILMENT: 8 of 8 criteria genuinely PASS-by-output or RECORDED (judgment) as literally cut
(F87-AC1/AC2/AC3/AC4/AC5/AC6/AC7 PASS; F87-AC8 judgment recorded with no verdict). F87-AC5 and F87-AC7
initially FAILed on this worker's first pass (order defects, reported not self-graded past, row
`IRPT_FNTEND-W37-S1`); the issuing COO amended both criteria's invocations, independently re-verified
them live, and this worker re-ran both amended invocations itself with matching results before this
flip.

## Rows filed

- **`IRPT_FNTEND-W37-S1`** (BLOCKING, disarm_owner `2.0.0_SA_COO~F`) -- **DISARMED.** F87-AC5's original
  literal invocation paired `--inject-css` with `--expect-ground` in one call; `scripts/ui-smoke.mjs`
  applies inject-css unconditionally before any ground measurement, so the invocation could only ever
  print the post-inject (wrong-ground) reading, never the pre-inject `PASS rgb(255, 255, 255)` the
  criterion's own `<expect>` required; F87-AC7's literal whole-suite invocation could not distinguish a
  real regression on this cell's surface from the sibling-cell FE-s-85 fixture gap every round-14 worker
  reads in isolation. The issuing COO amended F87-AC5's invocation (task-order file, this worker's own
  worktree copy) and independently re-verified it live; this worker re-ran it itself with a matching
  result (F87-AC5 above). F87-AC7's amendment-1 filter was itself found broken by the issuing COO
  (ANSI codes not suppressed by `NO_COLOR=1` here, plus a hyphen/space mismatch in the exclusion pattern)
  and corrected under **amendment 2** (ANSI-strip via `sed`, exclude on token `F81-AC3/AC4`); this worker
  re-ran the amendment-2 text itself with a matching result, positive-controlled (raw `✗` count = 2 post-
  strip, both excluded) (F87-AC7 above) -- row DISARMED per the amendments' own stated condition (order
  re-run and flipped complete).

## Portal commits

`AnswerStatus.tsx` (the two font-weight classes, nothing else). Committed at portal `393adf1d`, LOCAL on
branch `wk-irpt_fntend-14-87-fe-s-87-portal` (portal frozen); not pushed.

## Workspace commits

Surprise row `IRPT_FNTEND-W37-S1` (INVESTIGATION_v2.md), this proof-of-spec instance, this result file,
seven committed PNG captures under this worker's deliverables folder (`f87_ready_state_700.png`,
`f87_wrong_state_negative_control.png`, `f87_qualifier_400_and_state_700.png`,
`f87_ground_positive.png`, `f87_ground_wrong.png`, `f87_absent_qualifier_control.png`, plus the two
now-superseded diagnostic captures `f87_ground_and_wrong_ground.png` and
`f87_ground_diagnostic_no_inject.png` kept for the record). LOCAL on branch
`wk-irpt_fntend-14-87-fe-s-87`, not pushed.

## `<status>`

**Flips to `complete`.** F87-AC1/AC2/AC3/AC4/AC5/AC6/AC7 genuinely PASS by output; F87-AC8 (judgment)
RECORDED with no self-graded verdict. F87-AC5 and F87-AC7 originally genuinely FAILed by their own
`<expect>` as literally first cut (order defects, reported not self-graded past, row
`IRPT_FNTEND-W37-S1`); the issuing COO amended F87-AC5's invocation once and F87-AC7's invocation TWICE
(amendment 1's own filter was itself broken -- ANSI codes not suppressed, exclusion-pattern hyphen/space
mismatch -- caught and corrected under amendment 2) in the task-order file (and this worker's own
worktree copy), independently re-verifying each corrected invocation live, and this worker re-ran every
amended invocation itself with matching results (see F87-AC5/AC7 above and the updated proof-of-spec
instance). Per the standing bar, `<status>` flips to `complete` when every mechanical criterion is
PASS-by-output and the judgment criterion is RECORDED -- confirmed by `proof-of-spec-check.py` on the
updated instance.
