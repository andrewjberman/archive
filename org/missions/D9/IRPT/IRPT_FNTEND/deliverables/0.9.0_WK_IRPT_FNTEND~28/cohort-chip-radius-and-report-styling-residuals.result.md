# IRPT_FNTEND.TO-FE-s-78 -- result (0.9.0_WK_IRPT_FNTEND~28)

These captures are FIXTURE-FED: the real `investor-reporting` route, served by this worktree's own
`vite` dev server (port 5940, this worker's own block), with every backend request answered at the
network layer by `scripts/ui-smoke.mjs`'s own router (a declared `--fixtures` JSON map) -- no live
route, no live backend, was ever reached. The one exception, disclosed rather than hidden: the
`directory-search` fixture key in `cohort-selected.json` is never actually HIT by F78-AC2's own
literal invocation (see below) -- its truthfulness is proven separately, at the render level, in
`__tests__/fe-s-78/cohort-chip.test.ts`, through the SAME real `parseIrEnvelope` + `adaptDirectoryEntry`
+ `toOptionRow` pipeline the running page uses, never a hand-built view object.

## The fix

1. **`header/ScopeSummary.tsx:125` (W18-S1).** The cohort-chip `<button>` gains `data-slot="cohort-chip"`
   (it carried none before) and its radius moves from `rounded-md` (Tailwind's arbitrary-value-free
   4px-scale name, but this codebase's own class list makes it read as the literal C11-violating 6px
   token) to `rounded-[2px]` -- C11's `rounded.xs`, the clause's own value for "chips and tags". Kept the
   file's existing arbitrary-value idiom (`text-[10px]`, `text-[11px]` already sit beside it) rather than
   guessing at a Tailwind scale name, so the radius is unambiguous regardless of the project's Tailwind
   config.
2. **Truthful fixture, `__tests__/fe-s-78/fixtures/cohort-selected.json` (new).** A real
   `cohort.authoritative: true` `DirectoryEntryWire` (`fee_taking_status: OPAL_SUPERVISED`,
   `advisory_status: ADVISED`) served at `/api/scoped/investor-reporting/directory/search`, alongside
   the `resolve-scope`/`performance`/`holdings` triad `reporting-answer-bearing.json` already
   establishes (reused, not re-typed).
3. **`render/print.css` (C-S150).** The `@media screen { .ir-page { box-shadow: ... } }` rule removed
   outright. `ReportingTab.tsx` imports this file and puts `ir-page` on `[data-slot="reporting-body"]`
   -- the LIVE screen render, not only a print preview -- so this was a genuine on-screen drop shadow,
   which C11 bans outright ("No drop shadows... the focus ring is the only box-shadow in the product").
   `@media print`'s own `.ir-page { box-shadow: none; }` on the identical selector already made the
   screen rule's effect redundant once removed; nothing else depended on it.
4. **`__tests__/fe-s-78/scroll-exercise.mjs` (new, supplementary instrument).** `scripts/ui-smoke.mjs`
   carries no scroll flag and sits outside this cell's `<paths>` -- adding one there would be a wider
   grant this cell does not hold. This standalone script (same Playwright-core + Edge + fixture-router
   technique, not shared code) drives the SAME live route to actually exercise a horizontal scroll at
   390px width, since a `fullPage:true` capture (what `ui-smoke.mjs` saves) only extends vertically and
   cannot show whether horizontally-clipped content is reachable.
5. **`__tests__/fe-s-78/cohort-chip.test.ts` (new).** Render-level proof that (3), the fixture, and (1),
   the component fix, are correct together, independent of F78-AC2's own gap (below): the fixture's
   `directory-search` body parses through the real adapter to an authoritative cohort; `ScopeSummary`
   given that row mounts `data-slot="cohort-chip"` at the admitted radius, never `rounded-md`; and a
   `null` row (the exact shape F78-AC2's own invocation exercises) mounts no chip. `3 pass`.

## Acceptance (this worktree, dev server port 5940, `IRPT_FE_DEV_PORT` set only while the server ran)

- **F78-AC1** (whole portal typechecks): `$ tsc -b --noEmit` / `rc=0` -- **PASS**
- **F78-AC2** (cohort chip mounts at an admitted radius): run VERBATIM --
  `EXPECT[[data-slot="cohort-chip"]]: FAIL (0 visible)`, `EXPECT-STYLE[...]: UNMEASURABLE (selector
  matched nothing)`, `ASSERT-CONTENT: 0 of 1 met`, `ASSERT-STYLE: 0 of 1 met`,
  `FIXTURE-DEAD: /api/scoped/investor-reporting/directory/search` -- **FAIL, measured** (row
  `IRPT_FNTEND-W28-S1`; the invocation performs no click/fill, so `row` never leaves `null` and the
  fixture, however truthful, is never reached; see `cohort-chip.test.ts` for the render-level proof
  that the fixture and the fix are both genuinely correct)
- **F78-AC3** (content control: unrelated fixture mounts no chip): `EXPECT[[data-slot="cohort-chip"]]:
  FAIL (0 visible)`, `ASSERT-CONTENT: 0 of 1 met` -- **PASS-by-output**, but CONFOUNDED this round (row
  `IRPT_FNTEND-W28-S3`): it reads 0 for the SAME structural reason AC2 does (no interaction ever
  occurs), not because its fixture specifically withholds a cohort -- it does not yet discriminate
  between "no cohort in the fixture" and "no interaction happened"
- **F78-AC4** (screen box-shadow removed): `EXPECT-STYLE[[data-slot="reporting-body"]::box-shadow]:
  PASS none`, `ASSERT-STYLE: 1 of 1 met` -- **PASS**. Wrong-state control (own `--inject-css` re-adding
  the exact removed value): `EXPECT-STYLE[...]: FAIL rgba(10, 23, 51, 0.1) 0px 2px 16px 0px`,
  `ASSERT-STYLE: 0 of 1 met` -- discriminates. Absent-selector control (`fixtures/smoke/default.json`,
  no report body renders): `EXPECT-STYLE[...]: UNMEASURABLE (selector matched nothing)` -- discriminates.
- **F78-AC5** (390-width reachability, real scroll exercised): `EXPECT[[data-slot="reporting-body"]]:
  PASS (1 visible)`, `ASSERT-CONTENT: 1 of 1 met` -- **PASS-by-output**, though this specific mechanical
  check only confirms the container is visible (true regardless of internal clipping) and performs no
  scroll itself. The substantive exercise ran separately (`scroll-exercise.mjs`, see below) and is the
  real evidence for AC7's judgment.
- **F78-AC6** (whole suite green): `626 pass`, `22 skip`, `4 fail`, `2641 expect() calls`,
  `Ran 652 tests across 120 files` -- **FAIL, measured** (row `IRPT_FNTEND-W28-S2`). The 4 reds are
  `fe-s-42/every-site.test.ts F42-AC3`, `fe-s-48/withheld.test.ts F48-AC2` and `F48-AC3`,
  `fe-s-59/scope-summary-badge.test.ts F59-AC4` -- three files entirely outside this cell's `<paths>`
  grant, each hardcoding the OLD byte-exact chip markup (`class="rounded-md ..."`, no `data-slot`).
  Confirmed via `git show HEAD:.../ScopeSummary.tsx` that these strings match the PRE-FIX state
  exactly, so the breakage is caused entirely by this cell's own (required) radius fix, not
  pre-existing. No admitted-radius choice avoids this: F78-AC2 requires a value that is NOT 6px; the
  other three files' tests assert byte-exact equality to the 6px string. Not fixed (outside grant);
  reported honestly rather than narrowed or suppressed.
- **F78-AC7** (judgment, graded by the CVO at L9): RECORDED, no verdict taken. See "Substantive scroll
  exercise" and "Cohort chip, genuinely" below for the evidence this judgment should weigh.

## Substantive scroll exercise (F78-AC5's real evidence)

`scroll-exercise.mjs` against `reporting-answer-bearing.json` at 390px width:
- `BEFORE`: `[data-slot="reporting-body"]` `scrollWidth=948`, `clientWidth=310` -- a real 638px of
  horizontal overflow on the container itself (not a nested sub-scroller).
- A real `scrollBy({left: 638})` on that element: `scrollLeft` measured `638` afterward (the scroll
  genuinely moved the DOM's own scroll position, not merely computed a capacity number).
- A targeted, viewport-clipped (`page.screenshot({clip:...})`) before/after pair of the "Accounts in
  this report" table, at a smaller, non-destructive 140px scroll (the full 638px scroll moves the whole
  shared axis far enough that this particular table -- narrower than the container's widest child, the
  chart -- scrolls entirely out of view instead of revealing its own clipped edge): BEFORE shows only
  `Account / Reference / Covered / Ending value (USD)`, its 5th column (`Period returns`, values like
  `0.0688`, `0.0791`) fully off-screen; AFTER (138px measured, requested 140px) shows that exact column,
  now visible. Content that was genuinely clipped is genuinely reachable by a genuine scroll -- not a
  permanent clip, and not merely measured for capacity.
- Images (exploratory, not named by any criterion, so not saved under `deliverables/`): read directly
  in-session rather than filed, per "keep your context small".

## Cohort chip, genuinely (F78-AC2/AC3's render-level proof)

`cohort-chip.test.ts`, `3 pass`:
- The fixture's `directory-search` body, parsed through the REAL `parseIrEnvelope` +
  `adaptDirectoryEntry`: `PARSED cohorts: [{"axis":"supervision","value":"opal-supervised",
  "authoritative":true},{"axis":"advisory","value":"advised","authoritative":true}]`.
- `ScopeSummary` given that row (via `toOptionRow`): `RENDERED: data-slot="cohort-chip" present=yes;
  rounded-md present=no`; `CHIP TAG: <button type="button" data-slot="cohort-chip" class="rounded-[2px]
  px-2 py-0.5 text-[11px] text-slate-900 ring-1 ring-slate-500/40 hover:ring-slate-700">`.
- `row=null` (the exact shape F78-AC2's own invocation exercises): no `data-slot="cohort-chip"` in the
  markup.

This proves the fixture and the fix are BOTH genuinely correct; the gap is entirely in F78-AC2's own
invocation (row `IRPT_FNTEND-W28-S1`), not in the fixture's truthfulness or the component's behaviour.

## Rows filed

- **`IRPT_FNTEND-W28-S1`** (BLOCKING, ARMED, disarm owner `2.0.0_SA_COO~F`). F78-AC2's invocation
  performs no click/fill/clicktext, but `ScopeSummary`'s cohort chip renders only from
  `row.entry.cohorts`, and `row` is set only by `ClientSearch`'s `onSelectionChange` after a real typed
  search + picked result -- no fixture alone can populate it, and `ResolvedScope` carries no `cohorts`
  field to fall back on. Also probed and recorded: an amended invocation adding `--fill 'Client
  search=...'` + `--clicktext '<name>'` cannot currently reach the control either --
  `scripts/ui-smoke.mjs`'s `--fill` requires `getByRole('textbox', ...)`, and `ClientSearch`'s catalyst
  Combobox input is not `role=textbox` (the fill call timed out even though "Client search" is a real,
  present accessible name) -- a related, second gap in the shared instrument, itself outside this
  cell's `<paths>`.
- **`IRPT_FNTEND-W28-S2`** (BLOCKING, ARMED, disarm owner `2.0.0_SA_COO~F`). This cell's required radius
  fix breaks 4 pre-existing tests in 3 other cells' out-of-grant files
  (`__tests__/fe-s-42/every-site.test.ts` F42-AC3, `__tests__/fe-s-48/withheld.test.ts` F48-AC2/AC3,
  `__tests__/fe-s-59/scope-summary-badge.test.ts` F59-AC4), each pinned to the OLD byte-exact
  `rounded-md` markup. No radius choice avoids this.
- **`IRPT_FNTEND-W28-S3`** (OBSERVATION, INERT). F78-AC3 mechanically PASSES but is CONFOUNDED this
  round: it cannot yet distinguish "fixture lacks a cohort" from "no interaction ever happened" (row
  S1's same structural cause). Becomes a genuine control once S1 is disarmed.

## Controls

**Wrong-state (F78-AC4).** `--inject-css` re-adding the exact removed box-shadow value onto
`[data-slot="reporting-body"]`: `EXPECT-STYLE[...]: FAIL rgba(10, 23, 51, 0.1) 0px 2px 16px 0px`,
`ASSERT-STYLE: 0 of 1 met` -- the assertion genuinely discriminates.

**Absent-selector (F78-AC4).** `fixtures/smoke/default.json` (no report body ever renders for this
route/state): `EXPECT-STYLE[[data-slot="reporting-body"]::box-shadow]: UNMEASURABLE (selector matched
nothing)` -- never a silent PASS/FAIL on a non-existent element.

**F78-AC2/AC3, own control (self-caught, before trusting the mechanical run).** Ran F78-AC2's exact
invocation first, unmodified, before authoring any workaround; only after it measured FAIL did I probe
(separately, not as the recorded/graded run) whether an amended invocation could succeed, to determine
whether the defect was in the fixture or in the invocation's own shape. It is the invocation's shape
(row S1), confirmed independently by `cohort-chip.test.ts`'s render-level PASS on the identical fixture
bytes.

## Portal commit
`portal/src/pages/InvestorReporting/header/ScopeSummary.tsx`, `render/print.css`, and new
`__tests__/fe-s-78/` (fixture, `cohort-chip.test.ts`, `scroll-exercise.mjs`). Committed at portal
`e9d801539d247d338ba5241df7f1e4ffe3a1a350`, LOCAL on branch `wk-irpt_fntend-12-78-fe-s-78-portal`
(portal frozen); not pushed.

## Workspace commits
Surprise rows `IRPT_FNTEND-W28-S1`/`-S2`/`-S3`, this proof-of-spec instance, this result file. LOCAL on
branch `wk-irpt_fntend-12-78-fe-s-78`, not pushed.

## `<status>`
Stays `pending`: F78-AC2 and F78-AC6 are measured, mechanical FAILs (rows filed above), and per this
order's own bound ("do not self-grade past a failure... an order defect is reported, and the issuer
amends it") the flip to `complete` is not taken.
