# DSGN_IRPTV1.TO-IV-e-19 -- session log, 0.9.0_WK_DSGN_IRPTV1~11

## What was built

- `portal/DESIGN.md` -- clause C14, "Progressive disclosure is portal law", its own
  DSGN_REBRND commit (3cee4341). States the imperative, a MECHANISM (the closed vehicle
  still carries its content in server-rendered markup, so no fact is lost, only
  relocated) and a NON-APPLICATION (a control that operates directly on the one main
  picture in place stays beside it; `PanelHeader`, the band and the four empty states are
  chrome, not disclosable content). One matching "Don't" bullet added.
- `ReportingTab.tsx` -- `PerformanceHeadline` + `PerformanceChart` stay on the face as the
  headline and the ONE main picture; `ReturnsHeatmap` and `AccountsTable` now mount inside
  a new closed `<details data-slot="reporting-more-disclosure">` ("Monthly returns and
  accounts"), the same vehicle IV-e-18's "Report details" toggle already established.
  Neither moved component's own props or behaviour changed.
- `HoldingsTab.tsx` -- `HoldingsSummary` + `DrillTree` (with its `AccountFilter` control)
  stay on the face; `AllocationBars`, `HoldingsTreemap` and `SecurityList` now mount inside
  a new closed `<details data-slot="holdings-more-disclosure">` ("More holdings views").
  `HoldingsQualification` moved inside the existing "Report details" toggle beside
  `AnswerStatus` (both system facts, not the headline or the main picture).
- Three new tests under `__tests__/dsgn-irptv1/` (none existed before this order):
  `iv-e-19.at-rest.test.ts`, `iv-e-19.opens.test.ts`, `iv-e-19.design-clause.test.ts`.

## Design decision and its bound

`AllocationBars` gives each L0 category bar its OWN native per-bar `<details>`, nested
inside the new `holdings-more-disclosure` toggle. A naive non-greedy `<details>...\/details>`
regex closes on the FIRST nested `</details>` and truncates the outer block -- both new
tests instead use a depth-tracked scanner (`detailsBlocksOf`) that walks every
`<details`/`</details>` tag position with a counter, so a top-level block's boundaries are
correct regardless of what it nests.

`DrillTree` (with its pie/donut) was kept as the Holdings tab's ONE main picture, not moved
behind a toggle, specifically because a real-browser Playwright driver from an earlier round
(`__tests__/fe-s-32/holdings-driver.mjs`) measures that donut's drawn sector/label geometry
assuming it renders without a click; a closed `<details>` is `display:none` in a live
browser (unlike server-rendered markup, which still carries a closed block's bytes), so
hiding it there would have silently broken that pinned capture. This shaped the main-picture
choice; it did not require touching that driver or its own test.

## No-regression checks

- Full `__tests__/dsgn-irptv1/` suite: 68 pass / 1 fail (69 tests, 55 files). The 1 failure,
  `iv-e-10.ruled-touch.test.ts` (IVE10-AC3, a fixed-base `git diff --numstat` bound on
  `HoldingsTab.tsx` from an earlier cell), was already failing before this order touched
  anything (measured: 12 added/1 removed at df5e41b5, already outside its own <=2-added
  bound); this order's own in-grant edit grows the count further (39/5). Row
  DSGN_IRPTV1-W11-S3.
- `fe-s-5/` suite: 22 pass / 3 fail, identical count to a disposable `git worktree add` at
  the untouched df5e41b5 commit (symlinked `node_modules` so the suite could run) -- same
  three pre-existing failures rows DSGN_IRPTV1-W11-S1/S2 already documented, not new.
- `iv-e-17.regenerated.test.ts` (runs `tsc -b --noEmit` over the whole portal): 1 pass / 0
  fail after fixing an early draft's `node:child_process`/`node:path` imports (this
  program's tsconfig excludes `@types/node`; `node:child_process` carries only the members
  an existing ambient shim declares -- `execSync`, not `execFileSync`/`spawnSync`'s fuller
  signature -- and `node:url`'s `fileURLToPath` replaces `node:path` entirely).

## Mutant + determinism controls

- Mutant: added an `open` attribute to `holdings-more-disclosure`'s `<details>` (sed, in
  place); IVE19-AC1 failed with the expected leaked-slot / open-details arms; file restored
  byte-for-byte (`git diff --stat` empty) and the test re-ran clean.
- Determinism: all three tests run twice in a row post-restore, identical VERDICT lines
  both times.

## Surprises filed

- `DSGN_IRPTV1-W11-S3` -- the ruled-touch bound `iv-e-10.ruled-touch.test.ts` pins on
  `HoldingsTab.tsx` was already broken by an earlier cell's own in-grant edit before this
  order started, and this order's own in-grant edit necessarily grows it further.
