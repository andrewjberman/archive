# IRPT_FNTEND.TO-FE-s-76 -- result (0.9.0_WK_IRPT_FNTEND~26)

**FIXTURE-FED, NOT LIVE.** Every capture below (F76-AC2..AC4) answers `src/pages/InvestorReporting/
fixtures/smoke/fe-s-18-holdings-observed.json` served AT THE NETWORK LAYER through `scripts/
ui-smoke.mjs --fixtures`; no live backend route was reached. That is the right evidence for this
card: the CTO's ruling on the breadcrumb ink and the panel-border removal is a claim about RENDERING
under a known, named state (a fixed fixture, a fixed click path), not about live data correctness.
The component-level test (F76-AC6) is narrower still: it seeds `PanelError` and the pure guard
predicates (`revisionMismatch`/`canRenderDrill`) directly, and explicitly does NOT claim any browser
session (fixture-fed or live) can reach the revision-mismatch state -- see finding 3 below and the
row this cell's own BOUNDS points at (`IRPT_FNTEND-W17-S1`).

## Base and mechanics

- Workspace at the round-12 issuance commit on CLOUD (branches from `17a0ae65b4`); portal DEV
  `7b7215f0` plus FE-s-74's hardened `ui-smoke.mjs` instrument, already in this worktree's base.
- Dev server: `IRPT_FE_DEV_PORT=5926 bun run dev --port 5926` (port verified free via `curl` --
  `curl_rc_before=000` -- before starting, verified closed via `curl` -- `after_kill=000` -- after
  stopping). F76-AC2..AC5 ran with the server up; F76-AC1, F76-AC6 and F76-AC7 do not touch the dev
  server. F76-AC7 (the whole-suite bar) ran AFTER the server was stopped and its port confirmed
  closed, in a shell with `IRPT_FE_DEV_PORT` unset.
- Read `portal/DESIGN.md` C1..C12 and `portal/CLAUDE.md` in full before starting; PRD FWD-12's
  ENDPOINT row, `REMEDIATION_v8.md` @631b1308cb and `IRPT_FNTEND-W17-S1`
  (`surprise-channel/investigations/INVESTIGATION_v2.md`) read at HEAD.

## Fixes made (BEFORE/AFTER, one per finding, cited to clause)

1. **`tabs/holdings/DrillTree.tsx` breadcrumb, `:178-207` pre-fix (C8, DESIGN.md :352-361).**
   BEFORE: every segment was a `<button>` with `className="text-[hsl(var(--primary))] underline"`
   -- indigo ink, at-rest underline, no distinction between the CURRENT node and its ancestors.
   AFTER: every segment is navy (`text-[hsl(var(--palette-navy))]`); the LAST path entry (the
   current node -- `breadcrumbPath` returns root..target INCLUSIVE, confirmed at `slices.ts:157-168`)
   renders as a plain `<span data-slot="holdings-breadcrumb">` with `font-semibold`, never a link;
   every earlier entry stays a `<button data-slot="holdings-breadcrumb">` with
   `hover:underline focus:underline` (no at-rest underline). The focus ring is left unstyled on
   purpose -- `src/index.css`'s global `:focus-visible` rule already paints it indigo (C11), so
   nothing here removes or duplicates it. This also resolves the open judgment call FE-s-67 recorded
   for the CVO (navy, not purple). MEASURED (F76-AC2): `EXPECT-STYLE[[data-slot="holdings-
   breadcrumb"]::color]: PASS rgb(22, 51, 114)` on the sole rendered segment (the fixture's initial
   `currentRef` is root, so `path` has exactly one entry -- the CURRENT span, confirmed by reading
   `f76_breadcrumb_navy.png`: "A-0001" renders in navy, no underline, no purple). WRONG-STATE /
   ABSENT-SELECTOR CONTROL (F76-AC3, part e): without `--click Holdings` the tab never mounts
   `DrillTree` at all, so `ASSERT-CONTENT: 0 of 1 met` -- confirmed genuinely absent, not merely
   unstyled (`f76_breadcrumb_absent.png` read: REPORTING tab shown, no Holdings breadcrumb anywhere).

2. **`components/CategoryViewTree.tsx:944` pre-fix (C8 -- "not a chip fill, not a panel border").**
   BEFORE: `<div className="absolute inset-x-0 top-0 h-1 bg-[hsl(var(--palette-indigo))]" aria-hidden
   ="true" />` inside the light-ground card wrapper -- a full-width indigo top rule on every
   `CategoryOverview`/`CategoryTile` card. AFTER: the div is REMOVED entirely; the comment above the
   wrapper now names why (C8 :352-361, indigo spent on one persistent primary action plus six named
   identity places; a panel border is neither). MEASURED (F76-AC4): the selector
   `[data-slot="holdings-drill-tree"] section[aria-labelledby="asset-category-views"] >
   div:nth-of-type(2) > div > div` resolves (this path DID resolve, so no adaptation was needed) to
   what is now the FIRST direct `div` child of the light-ground wrapper -- the removed rule div used
   to be that first child (rendered before `{body}` in source order); with it gone, the same selector
   now reaches the next real element (`CategoryOverview`'s `<div className="relative mt-6 grid ...">`),
   which carries no explicit background and reads transparent: `EXPECT-STYLE[...background-color]:
   PASS rgba(0, 0, 0, 0)`, `!= rgb(95, 59, 227)`. CONTROL RUN (not a named criterion, run to confirm
   the assertion is not vacuous per the round's "a control is a claim" instruction): `--inject-css`
   forcing that same selector's `background-color` to `rgb(95, 59, 227)` flips the identical assertion
   to `FAIL rgb(95, 59, 227)`, `ASSERT-STYLE: 0 of 1 met` -- confirming the selector targets a real,
   measurable element and the PASS above is not vacuous. Both `f76_categoryview_1440.png` and
   `f76_breadcrumb_navy.png` (same capture, both criteria share one click path) show the "ALL
   CATEGORIES" card with no indigo top strip. The data palette (lilac/teal/amber pie slices, C6) and
   Model Portfolios' own dark-ground default (`ground="dark"`, untouched branch) are UNCHANGED --
   confirmed by reading the diff: only the `isLight` branch's wrapper lost the rule div.

3. **`components/CategoryViewTree.tsx:563` and `:670` pre-fix comments (C8 -- no generic
   "one accent link" exemption).** BEFORE, `:563-564`: *"The action link keeps its role (a text link)
   and re-hues to the site's indigo instead of the panel's lilac -- both are the ONE persistent accent
   this idiom names (C8)."* BEFORE, `:670`: *"...the light ground keeps the ONE accent text-link C8
   already permits."* Both assert a generic C8 exemption for an indigo text link that does not exist
   in C8's actual text (C8 names exactly one persistent primary action per view PLUS six identity
   places -- the page-title rule, header subtext, active tab, sidebar active item, rail edge, avatar --
   and "View breakdown" is none of those: not a filled button, not one of the six). AFTER: both
   comments now state the actual rule and name that the indigo colour choice on `linkColor`/"View
   breakdown" is left UNCHANGED only because recolouring it is outside this cell's grant (the BOUNDS
   name the `:936` rule and these two comment blocks ONLY) -- recorded for a future cell, not
   endorsed. MEASURED (F76-AC5): `grep -c 'one-accent-link' src/components/CategoryViewTree.tsx`
   prints `0`.

4. **W17-S1's component-level test, new file
   `src/pages/InvestorReporting/__tests__/fe-s-76/revision-mismatch-guard.test.ts` (F76-AC6).**
   `adaptHoldingsSnapshot` (`contracts/adapt.ts:938,965,981`) computes ONE `sourceSetRevision` local
   and assigns it to BOTH the snapshot's own field (:981) AND every node's `provenance.sourceRevision`
   (:965) -- the same expression, same call, every node. No wire payload this adapter ever produces
   can disagree with itself, so `DrillTree.tsx`'s revision-mismatch `PanelError` guard
   (`handleDrill` -> `canRenderDrill`/`revisionMismatch`, `slices.ts:198-210`) is structurally
   unreachable from any real fixture or backend response -- exactly as round 11's
   `IRPT_FNTEND-W17-S1` row already established. This test does NOT invent a wire field and does NOT
   claim browser reachability anywhere. It reuses (by READING, not editing -- out of this cell's
   grant) the existing hand-authored, already-VIEW-shape fixture `fe-s-7/holdings.stale-overlay.json`
   (`__tests__/fe-s-7/drill.test.ts` already asserts the pure predicate against it: `nd-stale`'s
   `provenance.sourceRevision` disagrees with the snapshot's own `sourceSetRevision`) rather than
   authoring a second synthetic instance, and adds what that file does not: rendering the REAL
   `PanelError` component (imported, unedited) with `renderToStaticMarkup` (no DOM, no jsdom/happy-dom/
   testing-library -- none are installed and this order forbids `bun install`, matching FE-s-16's own
   documented constraint) for the seeded refused node, asserting `data-panel-state="error"`,
   `role="alert"` and the exact refusal message text all render, a wrong-state control (a fresh
   sibling node does NOT trip the guard) and an absent-selector control (no refusal -> no
   `data-panel-state="error"` in the markup at all). A drift guard (test 1) reads `DrillTree.tsx`'s
   own source and fails if the literal message text this test asserts against ever changes there
   without this test being updated alongside it. `bun test .../fe-s-76`: 4 pass, 0 fail, 20 expect()
   calls.

## Criteria, verbatim

- **F76-AC1** (`bun run typecheck`): rc=0. PASS.
- **F76-AC2** (breadcrumb navy at-rest): `EXPECT[[data-slot="holdings-breadcrumb"]]: PASS (1
  visible)`; `EXPECT-STYLE[[data-slot="holdings-breadcrumb"]::color]: PASS rgb(22, 51, 114)`;
  `ASSERT-CONTENT: 1 of 1 met`; `ASSERT-STYLE: 1 of 1 met`. PASS.
- **F76-AC3** (absent-selector control): `EXPECT[[data-slot="holdings-breadcrumb"]]: FAIL (0
  visible)`; `ASSERT-CONTENT: 0 of 1 met`. PASS.
- **F76-AC4** (CategoryViewTree `:936` removal): `EXPECT-STYLE[...background-color]: PASS rgba(0, 0,
  0, 0)`; `ASSERT-STYLE: 1 of 1 met`. PASS (control run above confirms non-vacuous).
- **F76-AC5** (false comment removed): `grep -c 'one-accent-link' ...` -> `0`. PASS.
- **F76-AC6** (component-level revision-mismatch test): `bun test .../fe-s-76` -> `4 pass`, `0 fail`.
  PASS.
- **F76-AC7** (whole suite, server stopped, `IRPT_FE_DEV_PORT` unset): `631 pass`, `22 skip`, `0
  fail`, `2662 expect() calls`, `Ran 653 tests across 120 files`. PASS.
- **F76-AC8** (judgment, CVO): RECORDED above (findings 1-4); NO VERDICT given here.

## Surprises

None filed. No premise failed, no path was elsewhere, no invocation failed to produce its named
result, and no capability was missing -- every criterion in this cell's own grant was satisfiable
exactly as written, including the component-level test the cell anticipated could not be a browser
test.
