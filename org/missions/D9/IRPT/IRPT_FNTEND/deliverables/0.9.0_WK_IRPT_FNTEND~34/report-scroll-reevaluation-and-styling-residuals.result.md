# IRPT_FNTEND.TO-FE-s-84 -- result (0.9.0_WK_IRPT_FNTEND~34)

These captures are FIXTURE-FED: the real `investor-reporting` route, served by this worktree's own
`vite` dev server (port 5983, this worker's own wave-2 block 5980-5984), with every backend request
answered at the network layer by the fixture router (`scripts/ui-smoke.mjs`'s own mechanism, and
`__tests__/fe-s-80/scroll-exercise.mjs`'s adaptation of the same technique) -- no live route, no live
backend, was ever reached.

## Read first (HOW step 1)

`portal/DESIGN.md` C1-C12 in full, `portal/CLAUDE.md` in full, the PRD's FWD-12 ENDPOINT row
("The Investor Reporting screens look and behave like the rest of the Opal portal, so an advisor who
already uses the portal needs no re-learning", row F13 "design conformity ... narrow-viewport exercise
on the real route"), `REMEDIATION_v9.md:7` ("W17-S1 and C-S150 remain OPEN; no older bulk closure"),
and `ADJUDICATION_v4.md`'s F78-AC7 row ("The required 390px exercised-reachability artifact is
unreachable: committed f78_report_390_scrolled.png is the unscrolled literal visibility capture; the
result says exploratory before/after scroll images were not retained. A driver and reported
displacement do not supply the missing inspected pair. This is not a clipping FAIL; C-S150 remains
OPEN.") -- this is the exact gap Fix 1 closes: `__tests__/fe-s-78/scroll-exercise.mjs` (fe-s-78's own
result file, "Substantive scroll exercise" section) DID measure real overflow and DID scroll, but its
before/after pair was "exploratory ... not saved under deliverables/", so the CVO had nothing committed
to grade. Confirmed instrument landed (task order's own check): `__tests__/fe-s-80/scroll-exercise.mjs`
and `__tests__/fe-s-80/scroll-instrument.test.ts` are present in this worktree at round-13 vintage
(F80-AC4's own before/after pattern, reused verbatim below); `scripts/ui-smoke.mjs` still correctly
prints `UNMEASURABLE` on an absent selector for `--expect-style` (confirmed live below, AC4/AC5 absent
controls) -- base is current, not stale.

## Fix 1 -- F78-AC7 re-evaluated with a real, COMMITTED scroll exercise

`__tests__/fe-s-80/scroll-exercise.mjs` (reused verbatim, not a second driver -- its own header names
this cell as the reason it was built reusable) run against `[data-slot="reporting-body"]` -- the SAME
selector fe-s-78's own exploratory run measured overflowing -- at 390px, with `reporting-answer-bearing.json`
(the same fixture AC2 uses):

```
CAPACITY: {"scrollWidth":948,"clientWidth":310,"scrollLeft":0,"containerRight":374}
FAR-EDGE-BEFORE: {"left":112,"right":1012} CLIPPED
SCROLL-EXERCISED: {"before":0,"after":638,"target":638}
FAR-EDGE-AFTER: {"left":-526,"right":374} NOT CLIPPED
ASSERT-CONTENT: 2 of 2 met
DRIVER OK
```

Identical `scrollWidth`/`clientWidth`/scroll-target numbers to fe-s-78's own exploratory run (948, 310,
638) -- the same real overflow, now with a COMMITTED pair:
`f84_report_390_scroll_before.png` / `f84_report_390_scroll_after.png`. Read both myself (a grep cannot
see this): the BEFORE frame's "Accounts in this report" table shows only `Account | Reference | Covered
| Ending val[ue]` before the box clips (the 5th column and the chart's later x-axis dates,
`2026-04-01` through `2026-09-09`, are off-screen, matching the geometric CLIPPED read). The AFTER frame
(scrolled 638px, the geometric maximum) shows the far-edge element -- the cumulative-return chart's
right portion -- fully in view, with x-axis labels `2026-07-01`, `2026-08-03`, `2026-09-09` now visible
that were not present in the BEFORE frame at all (per fe-s-78's own note: a full-width scroll moves past
the narrower Accounts table, which is why AFTER shows chart, not that table's revealed column -- a
smaller, targeted scroll would show that instead, as fe-s-78's own 140px demo did; both are the same
container, the same real displacement, different scroll magnitude).

**The honest finding, per the order's own instruction not to invent a clipping defect:** the real scroll
reaches all content. Nothing is permanently cut off -- the far-edge element's CLIPPED state at rest
becomes NOT CLIPPED after a genuine, real `scrollLeft` displacement to the container's own
`scrollWidth - clientWidth` maximum. F78-AC7's re-evaluation is therefore clean: the Reporting tab's
390px report body is horizontally scrollable and everything in it is reachable by scroll, confirmed by a
COMMITTED before/after pair this time, not merely an in-session read.

## Fix 2 -- report styling residuals (C-S150)

`AnswerStatus.tsx:67-68`. Both states replaced with DESIGN.md-named roles, never invented:

- **Base/complete**: `border-slate-200` (`rgb(226,232,240)`, not a token) -> `border-[#C4CBDB]`
  (DESIGN.md `colors.mutedTint`, C3's panel-role hairline: "every container, marked by a 1px
  `palette.mutedTint` `#C4CBDB` hairline" -- also `portal/CLAUDE.md`'s own table: "panel ...
  `#FFFFFF` + `#C4CBDB` hairline"). `text-slate-900` -> `text-[#163372]` (DESIGN.md `colors.navy`,
  C3/C9: "primary text `palette.navy` `#163372`", 12.00:1 on a panel).
- **Qualified/warning**: `border-amber-500`/`bg-amber-50`/`text-amber-950` (none DESIGN.md-named) ->
  `border-2 border-[#D37C17]` (DESIGN.md `colors.status-warning`, the ONLY warning-named role the
  frontmatter carries) `bg-white` `text-[#163372]`. Per C6: "warning `#D37C17` measures 3.15:1 and is
  never text on a light ground -- it is an icon or fill beside navy text" -- so the warning role is
  carried on the BORDER only (3.15:1 clears the C9/SC-1.4.11 3:1 floor for a non-text state indicator),
  never as text, and the ground stays the C3 panel role (white), exactly the idiom `portal/CLAUDE.md`
  already names for a canvas-level status: "a `status.danger` icon beside navy text, never a red block
  or a translucent tint" (the same pattern `ErrorMessage.tsx`/`PanelError` use for the danger family).
  No amber/warm tint is invented; C5.8 ("output opacity is always 1.0... no translucent idiom") is
  honoured by using the solid named hex outright rather than a faded variant.

Both idioms use this codebase's existing arbitrary-value Tailwind convention for a literal DESIGN.md hex
(`ExportModal.tsx`/`PeriodControls.tsx` already use `border-[#163372]`, `text-[#163372]`,
`bg-[#F4F6FA]` the same way), rather than guessing at a Tailwind theme-scale name, per fe-s-78's own
precedent for the same reasoning ("kept the file's existing arbitrary-value idiom ... rather than
guessing at a Tailwind scale name").

Read both rendered PNGs myself: `f84_answer_status_navy.png` (complete/"Ready" state) shows a white
panel, thin light-grey hairline border, navy "Ready" label and navy body text throughout -- no
noncanonical slate. `f84_answer_status_qualified.png` (qualified/"Partial" state, using the substitute
fixture below) shows the SAME white panel, an orange (`#D37C17`) 2px border reading clearly as a
warning, and navy text throughout ("Partial", "Qualified answer -- not a complete report", the reason
code) -- no amber-950 warm text, no amber-50 tinted fill. No summary card value was fabricated in either
capture: `Beginning value (USD)` / `Ending value (USD)` / `Period return` still print `UNAVAILABLE` with
their real `unavailableReason` in both states, unchanged from the wire.

## F84-AC5 AMENDED and RE-GRADED PASS (resumption pass, same worker line, post-amendment)

**The issuing COO (`2.0.0_SA_COO~F`) amended the order** (shared-tree commit `6e3d50ab44`), independently re-verifying the
fixture-substitution finding below and repointing F84-AC5's `<invocation>` fixture path from the nonexistent
`fixtures/smoke/fe-s-32/qualified.json` to this cell's own already-committed substitute,
`src/pages/InvestorReporting/__tests__/fe-s-84/fixtures/reporting-qualified.json` -- the SAME file this worker
authored and measured below as supplementary evidence, now the graded invocation itself. The amendment was pulled
into this worktree (cherry-pick of `6e3d50ab44`, FE-s-84's task-order file only -- the amendment's other file,
FE-s-82's task order, is outside this cell's grant and was left untouched). Confirmed by reading the amended
`<invocation>` line at `:107` of the task-order file: it now names the substitute path.

Re-ran the amended invocation verbatim (WS/PORT substituted only) against a live dev server (port 5983, fresh
start, this cell's own wave-2 block, port confirmed closed afterward): `EXPECT-STYLE[[data-slot="answer-status"]
::background-color]: PASS rgb(255, 255, 255)`, `ASSERT-STYLE: 1 of 1 met`, `FIXTURES-MATCH: matched 3 of 3`,
`KEY-VALIDITY: 3 of 3`, `rc=0` -- identical to both this worker's own original supplementary measurement and the
COO's independent re-verification. `python .tools/proof-of-spec-check.py` on the updated instance against the
amended governing order: `VALID (rc=0)`, 0 violations, `invocation-alignment: 6/6 comparable row(s) match modulo
placeholder expansion; 0 diverge`.

Row `IRPT_FNTEND-W34-S1` is DISARMED per its own stated disarm condition ("disarmed when the issuing COO amends
the order's `<invocation>` fixture path... and this worker (or a successor) re-runs and flips the TO complete") --
both halves of that condition are now met by this pass. The row's top label is left as originally filed
(never edited in place, per the channel's append-only rule); this section and the commit that carries it are the
disarming record, per the order's own instructions from the resuming COO.

## Original entry, for the record (row `IRPT_FNTEND-W34-S1`, BLOCKING, ARMED at filing time, now DISARMED above)

AC5's literal `<invocation>` names `fixtures/smoke/fe-s-32/qualified.json`; the order's own BOUNDS text
flags fixture names in AC2/AC4/AC5 as illustrative and says "if fe-s-32/qualified.json is not the right
fixture for the qualified state, use the correct one and say so in your result." That path does not
exist (`fixtures/smoke/` has no `fe-s-32/` subfolder), and no committed static fixture under
`fixtures/smoke/` gives the Reporting route's performance operation a qualified producer state either
(every performance-operation state checked across `fixtures/smoke/*.json`: READY or QUEUED only --
`fe-s-15-needs-correction.json`'s "needs-correction" is a HOLDINGS-only state; its performance operation
carries no `status` block at all). `__tests__/fe-s-40/band-at-390.test.ts`'s own `qualifiedReportingMap()`
independently confirms this gap: it builds a Reporting-qualified scenario in-memory (clone the frozen
map, override `performance.status.state`) rather than reading a static fixture, because none exists.

**I did NOT substitute the fixture path in the graded/recorded invocation.** Row `IRPT_FNTEND-S31` (this
project's own prior finding, now built into `.tools/proof-of-spec-check.py`'s invocation-alignment limb)
rules that a corrected invocation must land in the task-order FILE, never only in a worker's
self-substituted proof record -- "the prompt is gone, the record is what the CVO grades." Confirmed
mechanically: recording the substituted invocation as F84-AC5's graded row makes the proof instance
`INVALID (rc=1)`, `VIOLATION: invocation-alignment[F84-AC5]`. So F84-AC5's graded row runs the LITERAL
invocation verbatim (`<WS>`/`<PORT>` substituted only, the order's own declared `<placeholders>`), and
it genuinely crashes: `Error: ENOENT: no such file or directory, open '...\fixtures\smoke\fe-s-32\
qualified.json'`, rc=1, no `EXPECT-STYLE`/`ASSERT-STYLE` line at all -- a real, measured FAIL against
the criterion's own `<expect>ASSERT-STYLE: 1 of 1 met</expect>` pattern.

Authored `__tests__/fe-s-84/fixtures/reporting-qualified.json` (inside this cell's own grant) as
SUPPLEMENTARY evidence only: a byte-identical copy of the committed `fixtures/smoke/reporting-answer-bearing.json`
with exactly one field changed, `performance.status.state`: `READY` -> `PARTIAL` -- the same one-field
technique `band-at-390.test.ts` already uses, made static because `ui-smoke.mjs --fixtures` reads a file
path. Ran the identical assertion against it separately (not as the graded row): `EXPECT-STYLE[[data-slot=
"answer-status"]::background-color]: PASS rgb(255, 255, 255)`, `ASSERT-STYLE: 1 of 1 met`,
`FIXTURES-MATCH: matched 3 of 3`, `KEY-VALIDITY: 3 of 3 valid consumed.ts operation keys` -- this proves
the STYLING FIX (Fix 2) itself is correct; only the order's literal fixture path needs a text amendment
before F84-AC5 can be re-run and graded PASS.

Row filed `IRPT_FNTEND-W34-S1`, class **BLOCKING**, hazard_standing **ARMED**, disarm_owner
`2.0.0_SA_COO~F` -- disarmed when the issuing COO amends F84-AC5's `<invocation>` fixture path to
`portal/src/pages/InvestorReporting/__tests__/fe-s-84/fixtures/reporting-qualified.json` (already
committed) and the TO is re-run and flipped complete.

## Acceptance

- **F84-AC1** (whole portal typechecks): `$ bun run typecheck` (= `tsc -b --noEmit`, per
  `portal/CLAUDE.md`'s typecheck law -- never the bare form) / `rc=0` -- **PASS**
- **F84-AC2** (before-scroll baseline, 390px unscrolled): `EXPECT[[data-slot="reporting-body"]]: PASS
  (1 visible)`, `ASSERT-CONTENT: 1 of 1 met`, `FIXTURES-MATCH: matched 3 of 3`, `KEY-VALIDITY: 3 of 3
  valid consumed.ts operation keys` -- **PASS**. PNG read: the "Accounts in this report" table's 4th
  column visibly truncates at the container's right edge, consistent with the measured 638px overflow.
- **F84-AC3** (real scroll exercise proves genuine displacement + reveal):
  `src/pages/InvestorReporting/__tests__/fe-s-84/report-scroll-exercise.test.ts`, built this cell,
  invoking FE-s-80's reusable driver against `[data-slot="reporting-body"]` at 390px --
  `SCROLL-EXERCISED: {"before":0,"after":638,"target":638}`, `FAR-EDGE-BEFORE: ... CLIPPED`,
  `FAR-EDGE-AFTER: ... NOT CLIPPED`, `ASSERT-CONTENT: 2 of 2 met`, `2 pass, 0 fail` -- **PASS, genuine**
  (dev server MET on port 5983, worktree-byte-matched by `probeDevServer`).
- **F84-AC4** (base/complete state measures navy ink, non-slate border):
  `EXPECT-STYLE[[data-slot="answer-status"]::color]: PASS rgb(22, 51, 114)`,
  `EXPECT-STYLE[[data-slot="answer-status"]::border-color]: PASS rgb(196, 203, 219)`,
  `ASSERT-STYLE: 2 of 2 met`, `FIXTURES-MATCH: matched 3 of 3`, `KEY-VALIDITY: 3 of 3` -- **PASS**.
  Controls (below) discriminate.
- **F84-AC5** (qualified state's background no longer amber-50): AMENDED by the issuing COO to the
  substitute fixture (`__tests__/fe-s-84/fixtures/reporting-qualified.json`); re-run against the amended
  `<invocation>` verbatim: `EXPECT-STYLE[[data-slot="answer-status"]::background-color]: PASS
  rgb(255, 255, 255)`, `ASSERT-STYLE: 1 of 1 met`, `FIXTURES-MATCH: matched 3 of 3`, `KEY-VALIDITY: 3 of 3`,
  `rc=0` -- **PASS**. See "F84-AC5 AMENDED and RE-GRADED PASS" above. Row `IRPT_FNTEND-W34-S1` DISARMED.
- **F84-AC6** (whole suite green): dev server stopped first (`curl` confirmed port 5983 closed, `000`),
  `IRPT_FE_DEV_PORT` unset: `643 pass`, `26 skip`, `0 fail`, `2678 expect() calls`, `Ran 669 tests
  across 125 files` -- **PASS, genuine**. This cell's own AC3 test SKIPPED by name (precondition
  ABSENT, as designed), never a false pass or fail.
- **F84-AC7** (judgment, graded by the CVO at L9): RECORDED, no verdict taken. See "Fix 1" above for
  F78-AC7's re-evaluation evidence (a genuine exercise, committed this time, and the honest finding
  that nothing is permanently clipped) and "Fix 2" for the styling replacements, each cited to its
  DESIGN.md clause, with no invented token and no fabricated summary value.

## Controls (THE CRITERION RULE, parts c/e -- run separately, not part of the graded invocations above)

**F84-AC4 wrong-state.** `--inject-css` re-adding the exact removed values (`border-color:#E2E8F0`,
`color:#0F172A`, the slate-200/slate-900 RGB equivalents) onto `[data-slot="answer-status"]`:
`EXPECT-STYLE[...::color]: FAIL rgb(15, 23, 42)`, `EXPECT-STYLE[...::border-color]: FAIL rgb(226, 232, 240)`,
`ASSERT-STYLE: 0 of 2 met` -- discriminates.

**F84-AC4 absent-selector.** `fixtures/smoke/default.json` (no report body renders):
`EXPECT-STYLE[...::color]: UNMEASURABLE (selector matched nothing)`,
`EXPECT-STYLE[...::border-color]: UNMEASURABLE (selector matched nothing)`, exit rc=1 -- never a silent
PASS/FAIL on a non-existent element.

**F84-AC5 wrong-state.** `--inject-css` re-adding the exact removed `background-color:#FFFBEB` (amber-50)
onto `[data-slot="answer-status"]`, against the qualified fixture: `EXPECT-STYLE[...::background-color]:
FAIL rgb(255, 251, 235)`, `ASSERT-STYLE: 0 of 1 met` -- discriminates.

**F84-AC5 absent-selector.** `fixtures/smoke/default.json`: `EXPECT-STYLE[...::background-color]:
UNMEASURABLE (selector matched nothing)`, exit rc=1 -- discriminates.

**Ground control (part d).** N/A for AC4/AC5 -- both use `--expect-style` measured directly on
`[data-slot="answer-status"]` itself (the element the assertion names), never `--expect-ground`'s
ancestor-walking reader; there is no page-field-vs-container ambiguity to control for. F78-AC4's own
precedent (box-shadow, also a bare `--expect-style` criterion) likewise carried no ground control.

**F84-AC2/AC3, own control.** Ran F84-AC2's literal invocation and F84-AC3's driver call first,
unmodified, before authoring anything else, to confirm the real overflow existed before trusting any
later assertion -- both measured the SAME numbers (948/310/638) fe-s-78's own exploratory run found,
corroborating rather than assuming the container's overflow.

## Rows filed

- **`IRPT_FNTEND-W34-S1`** (BLOCKING, ARMED, disarm_owner `2.0.0_SA_COO~F`). F84-AC5's literal fixture
  path does not exist; run verbatim it crashes (ENOENT), a genuine, measured FAIL. See "F84-AC5 REFUSED
  as literally cut" above. Disarmed when the issuing COO amends the order's `<invocation>` fixture path.

## Portal commits

New: `AnswerStatus.tsx` (styling fix), `__tests__/fe-s-84/report-scroll-exercise.test.ts`,
`__tests__/fe-s-84/fixtures/reporting-qualified.json`. Committed at portal (see hash below), LOCAL on
branch `wk-irpt_fntend-13-84-fe-s-84-portal` (portal frozen); not pushed.

## Workspace commits

Surprise row `IRPT_FNTEND-W34-S1` (INVESTIGATION_v2.md), this proof-of-spec instance, this result file,
five committed PNG captures under this worker's deliverables folder
(`f84_report_390_before_scroll.png`, `f84_report_390_scroll_before.png`, `f84_report_390_scroll_after.png`,
`f84_answer_status_navy.png`, `f84_answer_status_qualified.png`). LOCAL on branch
`wk-irpt_fntend-13-84-fe-s-84`, not pushed.

## `<status>`

**Flipped to `complete`.** The issuing COO amended F84-AC5's `<invocation>` fixture path (shared-tree
commit `6e3d50ab44`, pulled into this worktree); re-run against the amended invocation, F84-AC5 now
genuinely PASSes (`ASSERT-STYLE: 1 of 1 met`, rc=0). F84-AC1/AC2/AC3/AC4/AC6 stand as originally measured
(PASS), F84-AC7 (judgment) RECORDED with no self-graded verdict. `python
.tools/proof-of-spec-check.py <instance> F84-AC1,...,F84-AC7 --governing-order <amended TO>` ->
`VALID (rc=0)`, 0 violations. Every non-judgment criterion is PASS-by-output against the amended order, so
per the standing bar this TO now meets its order. Row `IRPT_FNTEND-W34-S1` DISARMED (see "F84-AC5 AMENDED
and RE-GRADED PASS" above).
