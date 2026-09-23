# IRPT_FNTEND.TO-FE-s-83 -- result (0.9.0_WK_IRPT_FNTEND~33)

**FIXTURE-FED, NOT LIVE.** Every capture/assertion below answers a fixture served AT THE NETWORK
LAYER through `scripts/ui-smoke.mjs --fixtures` (literal AC2/AC3/AC4 runs and their supplementary
adapted counterparts) or the same idiom through this cell's own
`__tests__/fe-s-83/hover-underline-driver.mjs`; no live backend route was reached at any point.

## THE HEADLINE FINDING FIRST: F83-AC2/AC3/AC4's LITERAL invocations FAIL, and the reason is an
## order defect, not this cell's fix (row `IRPT_FNTEND-W33-S1`, BLOCKING/ARMED)

The task order's own BOUNDS text says: *"Route/fixture in AC2-AC4 are illustrative -- CategoryViewTree
may mount under a different route than model-portfolios in this worktree; verify and adjust, the
requirement is the colour/underline discrimination, not these exact route/fixture names."* I initially
adapted the route (`investor-reporting` + `--click Holdings`) and fixture accordingly, per that
sentence, and confirmed the underlying fix works correctly that way.

**But `proof-of-spec-check.py`'s `invocation-alignment` limb does not read that sentence.** It reads
only the TO's `<placeholders>WS, PORT</placeholders>` declaration and mechanically REFUSES any
recorded invocation that diverges from the TO's literal `<invocation>` text beyond those two tokens
(`.tools/proof-of-spec-check.py:1394-1395,1412`). Running my adapted instance produced 3 hard
VIOLATIONs (F83-AC2/AC3/AC4) and `INVALID (rc=1)`.

I then ran the criteria's LITERAL invocations verbatim (route `model-portfolios`, only `<PORT>`/`<WS>`
substituted, nothing else changed) to see what the order, taken exactly as written, actually measures.
**The result is unambiguous: `model-portfolios` is not a real route at all.** `portal/src/App.tsx:
413-423` declares `/`, `/market`, `/portfolios` (the REAL Model Portfolios path), `/investor-reporting`,
`/philosophy`, etc. -- there is no `/model-portfolios`. Navigating there lands on `/market` (confirmed
by the instrument's own `LOC : /market <-- DID NOT LAND` diagnostic), 0 of 9 declared fixtures ever
match a URL, and every `--expect-style` assertion against `[data-slot="view-breakdown-link"]` reads
`UNMEASURABLE (selector matched nothing)` -- because the page that actually loads makes no
investor-reporting API calls and mounts no category tiles whatsoever.

Independently, even the CORRECT route name would not reach this fix: `ModelPortfolios.tsx:1286` mounts
`CategoryViewTree` with no `ground` prop, i.e. the DEFAULT `ground='dark'` -- a branch this cell's
grant explicitly excludes. The only caller passing `ground="light"` anywhere in the tree is
`DrillTree.tsx:244`, reached at `/investor-reporting` after clicking Holdings.

So F83-AC2 and F83-AC3's literal runs are genuine, unambiguous FAILs against their own `<expect>`
(0 of 2 / 0 of 1 met, not 2 of 2 / 1 of 1). F83-AC4's literal run prints the string `UNMEASURABLE`,
which textually satisfies its bare `<expect>UNMEASURABLE</expect>` regex -- but this is a **vacuous**
match: the label reads absent because the run never reaches any real page, not because this
fixture/route combination genuinely withholds the category tiles while otherwise rendering correctly.
Per this round's own HOW step 4 ("if a control passes when it should fail [or, as here, passes for an
unrelated reason], the assertion cannot tell the states apart: say so, never report it as met"), I
graded F83-AC4 FAIL rather than self-grade a vacuous match as a genuine absent-selector control.

**Filed `IRPT_FNTEND-W33-S1`** (BLOCKING, ARMED, `disarm_owner: 2.0.0_SA_COO~F`) citing all of this: the
route defect, the ground='dark' vs 'light' issue, and the conflict between the TO's own "illustrative"
permission and the mechanical gate's total refusal to honour it. I did not touch `scripts/ui-smoke.mjs`,
`ModelPortfolios.tsx`, or the task order file -- none are in this cell's `<paths>` grant.

**The underlying FIX is independently confirmed correct.** Every acceptance row below carries, in
addition to the literal (graded) run, a SUPPLEMENTARY section recording the adapted invocation's
genuine result -- clearly marked, never substituted for the graded row. `F83-AC1` and `F83-AC5` are
unaffected (their invocations name no route/fixture) and PASS cleanly.

## Base and mechanics

- Workspace at the round-13 issuance commit on CLOUD (branches from `3ebfc48ab2`); portal DEV
  `2d7b2f21` (round 12's close) plus FE-s-80's round-13 hardened `ui-smoke.mjs` instrument, already in
  this worktree's base -- confirmed via `scripts/ui-smoke.mjs`'s own `routeKeyCandidates`/`UNMEASURABLE`
  code and `git -C portal log --oneline -3` (FE-s-80's drain `eefb618015` at HEAD).
- Dev server: `IRPT_FE_DEV_PORT=5975 bun run dev --port 5975` (port verified free via `curl` --
  `000` -- before starting each time; verified closed via `curl` -- `000` -- after stopping, PID found
  via `netstat -ano`, `taskkill //PID <pid> //F //T`). F83-AC2..AC4 (literal and supplementary) and the
  hover driver ran with the server up; F83-AC1/AC5 do not need it up (F83-AC5 ran with the server
  stopped and `IRPT_FE_DEV_PORT` unset).
- Read `portal/DESIGN.md` C1..C12 and `portal/CLAUDE.md` in full before starting; PRD FWD-12's ENDPOINT
  row and the cell's own text (`CategoryViewTree.tsx:561-568`, FE-s-76's corrected comment establishing
  NO C8 exemption for this label) read at HEAD.

## Fixes made (BEFORE/AFTER, cited to clause)

1. **`components/CategoryViewTree.tsx:574` (linkColor, light branch) and `:677` (the label),
   C8/DESIGN.md :352-361.** BEFORE: `linkColor = isLight ? 'hsl(var(--palette-indigo))' : LILAC_LIGHT`,
   and the label carried no `data-slot`, no underline classes. AFTER: `linkColor`'s light branch is
   `hsl(var(--palette-navy))` (#163372, confirmed identical to `--palette-navy`'s own definition,
   `design/themes/opal-capital.css:23`); the label carries `data-slot="view-breakdown-link"` and
   `no-underline group-hover:underline group-focus-visible:underline` (no at-rest underline, matching
   `DrillTree.tsx`'s breadcrumb-link idiom -- `group-hover`/`group-focus-visible` here rather than
   `hover`/`focus` there, because THIS label is not independently focusable: the whole tile is the
   `<button>`, confirmed by reading `canDrill`'s definition -- `rows.length > 0 || Boolean(L0_COPY[name])`
   -- and that `DrillTree.tsx`'s adapter always emits empty `children`/`members`, so every tile carrying
   this label IS the button branch, confirmed empirically). The dark-ground branch (`LILAC_LIGHT`) is
   untouched. The focus RING is untouched: no ring/outline class was added or removed anywhere in this
   diff; `src/index.css:612-624`'s global unlayered `:focus-visible` rule already paints every focusable
   element's ring from `--semantic-action-primary` (`#5F3BE3`, the site indigo,
   `design/themes/opal-capital.css:94`), confirmed by reading that file.

2. **THE INSTRUMENT GAP -- `scripts/ui-smoke.mjs` has no generic hover-only mechanism, and a new
   driver was built within this cell's own grant to reach one.** Read in full: the only interaction
   flags are `--click`/`--clicktext`/`--fill`/`--pick` (all fire a real Playwright `.click()`) and
   `--hoverlast` (hard-wired to `.recharts-wrapper`, structurally unreusable for a category tile).
   MEASURED: every tile carrying this label is `canDrill: true` (see finding 1), so it is ALWAYS a
   `<button onClick={onOpen}>`; clicking it (via `--click` on its exact `aria-label`, confirmed with a
   scratch run) opens `HeroDialog`, whose full-viewport overlay becomes the topmost element under the
   pointer and measurably breaks the tile's `:hover` -- `EXPECT-STYLE[...text-decoration-line]` flips
   from a real hover's PASS to `FAIL none` on the IDENTICAL selector. `scripts/ui-smoke.mjs` is outside
   this cell's `<paths>` grant. Built `__tests__/fe-s-83/hover-underline-driver.mjs` instead --
   `playwright-core` direct, the established per-cell-driver idiom this suite already uses seven times
   (`__tests__/fe-s-19,30,31,32,40,58,77,78,80/*-driver.mjs`). It clicks the Holdings TAB (no onClick
   reaches `CategoryTile`'s button, so no dialog opens), then `page.hover()`s the label's closest
   `<button>` ancestor -- a genuine Playwright pointer move, no click in the chain -- and reads
   `text-decoration-line` off the SAME element before hover (none), during hover (underline), and after
   the pointer moves away (none again). Wrapped in `__tests__/fe-s-83/hover-underline.test.ts` using the
   suite's standard declared-precondition pattern (`__tests__/fe-s-27/_dev-server.ts`) so this new test
   SKIPS (0 failures) when the dev server is down -- the state F83-AC5 requires.

## Criteria, verbatim

- **F83-AC1** (`bun run typecheck`): `$ tsc -b --noEmit`, `rc=0`. PASS.
- **F83-AC2** (literal invocation, route `model-portfolios`, fixture `fe-s-18-frozen.json`): `LOC :
  /market`, `FIXTURES-MATCH: matched 0 of 9`, `EXPECT-STYLE[...color]: UNMEASURABLE` x2,
  `ASSERT-STYLE: 0 of 2 met` against `<expect>ASSERT-STYLE: 2 of 2 met</expect>`. **FAIL** (order
  defect, row `IRPT_FNTEND-W33-S1`). Supplementary adapted run (route `investor-reporting`, fixture
  `fe-s-18-holdings-observed.json`, `--click Holdings`): `EXPECT-STYLE[...color]: PASS rgb(22, 51,
  114)` (positive and negative), `ASSERT-STYLE: 2 of 2 met`. Capture `f83_view_breakdown_rest.png`
  (read directly: HOLDINGS tab, three tiles at rest, label present at opacity-0, no visible text --
  correct for the rest face).
- **F83-AC3** (literal invocation, no hover-triggering step at all): `LOC : /market`,
  `EXPECT-STYLE[...text-decoration-line]: UNMEASURABLE`, `ASSERT-STYLE: 0 of 1 met` against
  `<expect>ASSERT-STYLE: 1 of 1 met</expect>`. **FAIL** (same order defect, plus the literal invocation
  itself never simulates a hover). Supplementary own driver (`bun test __tests__/fe-s-83`,
  `IRPT_FE_DEV_PORT=5975`): `ASSERT-STYLE: 3 of 3 met` (rest=none -> hover=underline -> release=none),
  `1 pass/0 fail`, MUTANT CONTROL fired as expected and restored byte-identical. Capture
  `f83_view_breakdown_hover.png` (read directly: Models tile detail face, "View breakdown" in navy
  WITH visible underline and the arrow glyph).
- **F83-AC4** (literal invocation): `LOC : /market`, `EXPECT-STYLE[...color]: UNMEASURABLE`,
  `ASSERT-STYLE: 0 of 1 met` -- textually matches `<expect>UNMEASURABLE</expect>` but VACUOUSLY (see
  headline finding above). **FAIL** (graded FAIL despite the textual match, per HOW step 4). Genuine
  supplementary absent-selector control (route `investor-reporting`, fixture
  `fe-s-18-holdings-observed.json`, NO `--click Holdings`): `EXPECT-STYLE[...color]: UNMEASURABLE`,
  `ASSERT-STYLE: 0 of 1 met` -- absent for the RIGHT reason this time. Capture
  `f83_view_breakdown_absent_control.png` (read directly: REPORTING tab, Holdings never clicked, no
  category cards, no breakdown link anywhere).
- **F83-AC5** (whole suite, dev server stopped, `IRPT_FE_DEV_PORT` unset): `643 pass`, `25 skip`, `0
  fail`, `2678 expect() calls`, `Ran 668 tests across 125 files` (this cell's own
  `hover-underline.test.ts` is one of the 25 skips, printing its SKIPPED line by name, `0 failures`, not
  a code defect). PASS.
- **F83-AC6** (judgment, CVO): RECORDED above (findings 1-2) plus a note that the genuine mechanism
  evidence for this judgment lives in the SUPPLEMENTARY runs, not the literal (broken-route) ones; NO
  VERDICT given here.

## Surprises

**One row filed: `IRPT_FNTEND-W33-S1`** (BLOCKING, ARMED, `disarm_owner: 2.0.0_SA_COO~F`) --
F83-AC2/AC3/AC4's literal invocation route `model-portfolios` is not a real app route (redirects to
`/market`, 0 of 9 fixtures ever matched), and even the real route (`/portfolios`) would not reach this
cell's fix (`ModelPortfolios.tsx` mounts `CategoryViewTree` at its default `ground='dark'`; only
`DrillTree.tsx` passes `ground="light"`); the order's own BOUNDS text authorizes adapting the
route/fixture, but `proof-of-spec-check.py`'s `invocation-alignment` limb mechanically refuses any such
adaptation given the TO's `<placeholders>WS, PORT</placeholders>` declaration. See the row for full
grounding (citations at HEAD, both the mechanically-refused adapted run and the literal run's true
output).

## Proof instance (first pass)

Recording the LITERAL invocations (satisfying `invocation-alignment`) with honest FAIL statuses where
the literal run does not meet `<expect>` produces a STRUCTURALLY VALID instance:
`python .tools/proof-of-spec-check.py <instance> F83-AC1,...,F83-AC6 --governing-order <TO>` ->
`VALID (rc=0)`. This is NOT a met order -- F83-AC2/AC3/AC4 are genuinely FAIL on this instance, so
`<status>` stays `pending`, per the standing rule that a valid instance is not a met order.

## ADDENDUM (second pass, 0.9.0_WK_IRPT_FNTEND~33, 2026-09-22, post-COO-amendment)

`2.0.0_SA_COO~F` independently confirmed all three findings above (App.tsx's routes, `ModelPortfolios.tsx`'s
wrong-ground mount, `DrillTree.tsx:244` as the sole `ground="light"` caller) and amended the governing TO in
the shared tree (CLOUD commit `6d3b2e4d92`): F83-AC2 and F83-AC4's `<invocation>` text now names route
`investor-reporting`, fixture `fe-s-18-holdings-observed.json` (AC2 with `--click Holdings`, AC4 without --
matching this worker's own supplementary runs exactly), and F83-AC3's `<invocation>` now runs
`hover-underline.test.ts` directly instead of a raw `ui-smoke.mjs` call. No criterion's bar changed. Cherry-picked
`6d3b2e4d92` into this worktree branch (commit `953f6745ab`), read the amended criteria directly, and re-ran
each amended invocation VERBATIM (dev server on port 5975, stopped and port-closed-confirmed afterward):

- **F83-AC2**: `ASSERT-STYLE: 2 of 2 met` against `<expect>ASSERT-STYLE: 2 of 2 met</expect>`. **PASS.**
  `LOC : /investor-reporting`, `CLICKED: Holdings`, both the positive (navy) and negative (not-indigo)
  assertions read `PASS rgb(22, 51, 114)`.
- **F83-AC3**: `bun test .../hover-underline.test.ts` -> `1 pass`, `0 fail`, `ASSERT-STYLE: 3 of 3 met`
  (rest=none -> hover=underline -> release=none) against `<expect>(?<![0-9])0 fail</expect>`. **PASS.**
- **F83-AC4**: `EXPECT-STYLE[...color]: UNMEASURABLE (selector matched nothing)` against
  `<expect>UNMEASURABLE</expect>`, and this time GENUINELY so, not vacuously: `LOC : /investor-reporting`
  (the run actually landed on the real page, 3 of 9 fixtures matched real URL calls) with Holdings never
  clicked, so the category tiles never mount for the right reason. **PASS.**

Updated the proof-of-spec instance's F83-AC2/AC3/AC4 acceptance rows to PASS with these new invocations and
outputs (F83-AC1/AC5/AC6 left as they already stood, per instruction). Re-ran
`python .tools/proof-of-spec-check.py <instance> F83-AC1,...,F83-AC6 --governing-order <TO>` (amended TO) ->
`VALID (rc=0)`, `violations=0`, `invocation-alignment: 5/5 comparable rows match`. Every non-judgment
criterion now genuinely PASSES; `<status>` flipped to `complete`.

Row `IRPT_FNTEND-W33-S1` stays on file in `INVESTIGATION_v2.md` as the historical record of the order
defect this worker correctly surfaced rather than self-graded past (per this rule's own "never edit an
existing row" -- the row is not retracted, only its underlying cause is now fixed by the amendment).
