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
- **F87-AC5** (GROUND ON THE ACTUAL CONTAINER, control d) -- **FAIL, order defect, reported not
  self-graded past.** The literal invocation pairs `--expect-ground` with `--inject-css` in ONE call.
  `scripts/ui-smoke.mjs:437-442` applies every `--inject-css` unconditionally BEFORE the
  `--expect-ground` measurement loop at `:557-574` (confirmed by reading the source; flag order on the
  command line does not matter -- both arg lists are extracted by an order-independent `reduce()` over
  the whole `args` array, `:145-146`). So this exact invocation can only ever print the POST-inject
  ground reading, never a pre-inject one, and its single `EXPECT-GROUND` line reads
  `EXPECT-GROUND[[data-slot="answer-status"]]: FAIL rgb(196, 203, 219)`, `ASSERT-GROUND: 0 of 1 met`,
  rc=0 -- no `PASS rgb(255, 255, 255)` substring anywhere in the output, so the criterion's own
  `<expect>EXPECT-GROUND.*PASS rgb\(255, 255, 255\)</expect>` does not match. The cell text itself
  assumes a "SECOND EXPECT-GROUND line (post-inject)" exists in this capture, implying a first,
  pre-inject PASS line -- the tool does not produce one when both flags are given together. Filed as
  row `IRPT_FNTEND-W37-S1` (BLOCKING, ARMED, disarm_owner `2.0.0_SA_COO~F`). Ran a SEPARATE diagnostic
  (same fixture/selector/expect-ground value, `--inject-css` omitted, NOT the graded invocation, not
  self-substituted into the graded row per row `IRPT_FNTEND-W34-S1`'s own precedent) to confirm the
  underlying claim is true: `EXPECT-GROUND[[data-slot="answer-status"]]: PASS rgb(255, 255, 255)` --
  the container genuinely grounds white (C3's panel role) absent injection; only this criterion's
  literal single-invocation cannot demonstrate both the true-ground read and the wrong-ground control in
  one capture.
- **F87-AC6** (ABSENT-SELECTOR CONTROL, control e: qualifier badge genuinely absent on the
  answer-BEARING/complete=true fixture): `EXPECT-STYLE[[data-slot="answer-qualifier"]::font-weight]:
  UNMEASURABLE (selector matched nothing)`, `ASSERT-STYLE: 0 of 1 met` -- **PASS** (matches
  `<expect>UNMEASURABLE</expect>`; rc=1 per the script's own FE-s-74 fail-closed-on-unmeasurable design,
  unrelated to the text match). PNG read confirms the qualifier badge does not render on the complete
  state.
- **F87-AC7** (whole suite green) -- **FAIL, pre-existing, out-of-grant, already disclosed by the
  issuer.** Dev server stopped first (`curl` confirmed port 6003 closed, `000`), `IRPT_FE_DEV_PORT`
  unset: `648 pass`, `27 skip`, `2 fail`, `2704 expect() calls`, `Ran 677 tests across 127 files` --
  exactly the residual `REMEDIATION_v10.md:5` names at cut time ("648 pass / 27 skip / 2 fail. The two
  failures are committed sibling fixtures missing unprojected_grant"). Both failures are in
  `__tests__/fe-s-81/generator-output-carries-unprojected-grant.test.ts`, against
  `fixtures/smoke/fe-s-13-wire.json` (0 of 9 entries carry `unprojected_grant`) and
  `fixtures/smoke/fe-s-14-print-v1.json` (0 of 2) -- confirmed by reading the failing assertions
  directly. `git diff --stat` confirms this worker's ONLY change is `AnswerStatus.tsx`, 2 lines; neither
  failing file is touched by, or reachable from, a font-weight class change. Not in this cell's `<paths>`
  grant (`AnswerStatus.tsx` + `__tests__/fe-s-87/` only), and already a known residual the issuer
  disclosed before this order was cut -- not a new finding, so no new surprise row minted for it (see
  `IRPT_FNTEND-W37-S1` above for the one genuinely new finding this cell surfaced).
- **F87-AC8** (judgment, graded by the CVO at L9): RECORDED, no verdict taken. State-label weight
  measured 700, qualifier weight measured 400 on the same co-located capture (F87-AC4); the wrong-state
  control (F87-AC3) and absent-selector control (F87-AC6) both genuinely discriminate, confirmed above;
  the ground measurement targets `[data-slot="answer-status"]`, the actual panel container (C3's role),
  not the page canvas -- confirmed true by the supplementary diagnostic under F87-AC5, though the
  criterion's own literal invocation cannot demonstrate it in one capture (order defect, row
  `IRPT_FNTEND-W37-S1`).

## Controls (THE CRITERION RULE / C-S176, five controls)

- (a) WIRE MATCH -- F87-AC2's `FIXTURES-MATCH: matched 3 of 3`, `KEY-VALIDITY: 3 of 3` (every capture).
- (b) NAMED CONTENT -- F87-AC2 ("Ready", weight 700) and F87-AC4 (qualifier text + weight 400,
  co-located state weight 700).
- (c) WRONG-STATE NEGATIVE CONTROL -- F87-AC3, discriminates (0 of 1 met).
- (d) GROUND ON THE ACTUAL CONTAINER -- F87-AC5's literal invocation cannot demonstrate this in one
  capture (order defect, reported above); the underlying claim is confirmed TRUE by a separate
  diagnostic run, kept supplementary, never substituted into the graded row.
- (e) ABSENT-SELECTOR CONTROL -- F87-AC6, discriminates (UNMEASURABLE, not a vacuous PASS).

**DECLARED-KEY VALIDITY vs EXERCISED FULFILMENT, stated separately per C-S176 step 6:** all 8
`<expected_criteria>` keys parse in this instance (DECLARED-KEY VALIDITY: 8 of 8). EXERCISED
FULFILMENT: 6 of 8 criteria genuinely PASS by their own literal `<expect>` (F87-AC1/AC2/AC3/AC4/AC6,
plus the judgment row F87-AC8 recorded with no verdict); 2 of 8 genuinely FAIL as literally cut
(F87-AC5 -- order defect, control (d) unreachable by this exact invocation though the underlying claim
is true; F87-AC7 -- pre-existing 2-fail residual, out of grant, already disclosed at cut time). Neither
FAIL is self-graded past; both are reported with their measurement.

## Rows filed

- **`IRPT_FNTEND-W37-S1`** (BLOCKING, ARMED, disarm_owner `2.0.0_SA_COO~F`). F87-AC5's literal invocation
  pairs `--inject-css` with `--expect-ground` in one call; `scripts/ui-smoke.mjs` applies inject-css
  unconditionally before any ground measurement, so the invocation can only ever print the post-inject
  (wrong-ground) reading, never the pre-inject `PASS rgb(255, 255, 255)` the criterion's own `<expect>`
  requires. The underlying ground claim is confirmed true by a separate, non-graded diagnostic run.
  Disarms when the issuing COO amends F87-AC5's invocation/expect (e.g. two separate captures, or an
  `<expect>` matching the single post-inject FAIL line this tool actually produces) and the cell is
  re-run against the amended text.

## Portal commits

`AnswerStatus.tsx` (the two font-weight classes, nothing else). Committed at portal `393adf1d`, LOCAL on
branch `wk-irpt_fntend-14-87-fe-s-87-portal` (portal frozen); not pushed.

## Workspace commits

Surprise row `IRPT_FNTEND-W37-S1` (INVESTIGATION_v2.md), this proof-of-spec instance, this result file,
five committed PNG captures under this worker's deliverables folder (`f87_ready_state_700.png`,
`f87_wrong_state_negative_control.png`, `f87_qualifier_400_and_state_700.png`,
`f87_ground_and_wrong_ground.png`, `f87_absent_qualifier_control.png`). LOCAL on branch
`wk-irpt_fntend-14-87-fe-s-87`, not pushed.

## `<status>`

**Stays `pending`.** F87-AC1/AC2/AC3/AC4/AC6 genuinely PASS by output; F87-AC8 (judgment) RECORDED with
no self-graded verdict; F87-AC5 and F87-AC7 genuinely FAIL by their own `<expect>` as literally cut,
neither weakened nor self-graded past, both reported here and in the proof-of-spec instance with their
measurement. Per the standing bar, `<status>` flips to `complete` only when every mechanical criterion is
PASS-by-output -- two are not, so this order stays open pending the issuer's amendment of F87-AC5 (a tool-
mechanics mismatch, row `IRPT_FNTEND-W37-S1`) and F87-AC7's pre-existing, out-of-grant residual
(`REMEDIATION_v10.md`'s own disclosed 2-fail baseline, FE-s-81's surface).
