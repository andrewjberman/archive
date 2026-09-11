# IRPT_FNTEND.TO-FE-s-11 -- result

**Worker:** `0.9.0_WK_IRPT_FNTEND~1` · **Cell:** `FE-s-11` · **Branch:** `wk-irpt_fntend-1-7-fe-s-11`
(workspace HEAD at start `e23ab5d9d4`; portal HEAD at start `787015e8`) · **Push state:** LOCAL.

**F11-AC3 FAILS BY OUTPUT.** Every other mechanical criterion PASSES BY OUTPUT (F11-AC5/AC6/AC7
pass on their named bar, `rc=0`, with a genuine, disclosed defect in the CONTENT captured -- see
below and the two surprise rows). `F11-AC9` is a judgment criterion: its output is RECORDED here
and in the proof instance with NO verdict; the oracle is `3.0.0_SA_CVO` at L9. Because a mechanical
criterion fails, this task order's `<status>` is **not** flipped to `complete`.

## What was built

This order writes no portal code; its product is the record.

- `census.ts` (this folder) -- a real parser (regex-based import-edge extraction + JSX-usage
  detection + specifier resolution + PRD-reuse-row accounting), run with `bun run census.ts` from
  `portal`. It walks every `.tsx` file under `portal/src/pages/InvestorReporting/**` (excluding
  `__tests__/`, `fixtures/`) plus `portal/src/App.tsx` (for its two `React.lazy` mounts of this
  feature only -- disclosed in the script's own header, not the app shell's unrelated imports), and
  writes `component-census.json` + `component-census.md` beside itself. `COMPONENTS: 65 (REUSED 27,
  NEW 38)`; 2 components are exported but imported by nothing anywhere (`AppliedBranding`,
  `ReceiptPanel` -- surprise row `IRPT_FNTEND-W1-S11`); all 11 PRD PATHS-table reuse rows are
  accounted (6 used by import, 2 used by pattern-not-import with the mechanism named, 3 not used
  with a reason).
- `component-census.json` / `.md` -- the census output.
- `brand-review.md` -- the brand review. Its two named sources
  (`deck_generation/brand_spec/brand.json`, `deck_generation/brand/opal_brand_guidelines.pdf`) are
  ABSENT from every worktree (gitignored; confirmed `0 hit(s)` over the `raw` corpus, 76,056 files) --
  an ALREADY-FILED premise gap (`IRPT_FNTEND-W2-S1`), not re-filed here. The review uses the
  substitutes the codebase already provides for that exact reason (`render/brand.tokens.json`,
  `render/brand.ts`) plus `deck_generation/DESIGN_BIBLE.md` (present) as an independent corroborating
  source, and cites both this order's own screenshots and, where this order's own capture hit the
  crash below, an earlier cell's own already-committed working capture (read-only, for informational
  context, clearly labelled).
- `fe-s-11_page_390.png`, `fe-s-11_analysis_390.png`, `fe-s-11_holdings_390.png`,
  `fe-s-11_export_390.png`, `fe-s-11_print_390.png` -- the five named 390px captures.
- `portal/src/pages/InvestorReporting/__tests__/fe-s-11/census.test.ts` -- grades `component-census.json`
  cross-repo (every row REUSED-with-existing-path or NEW-with-non-empty-reason; every PRD reuse row
  used-or-reasoned; `definedButNotImported` entries are real files with no row of their own).
- `portal/src/pages/InvestorReporting/__tests__/fe-s-11/colour-law.test.ts` -- scans every `.tsx` file
  under the tree for `text-white` / `text-<colour>-300` / `bg-white/<opacity>` outside a same-file
  `<Panel>`/`variant="dark"` ancestor, a self-contained dark background on the same class string, or a
  Tailwind state-variant prefix (the WORKER FACE's own two anchors, plus two more this scan states and
  a reviewer can dispute -- see the test file's own header). Finds ONE genuine violation:
  `export/AppliedBranding.tsx:43`.

## Criteria, as run

| id | invocation | deciding output | denominator |
|---|---|---|---|
| F11-AC1 | `bun run census.ts; echo rc=$?` | `COMPONENTS: 65 (REUSED 27, NEW 38)`, `rc=0` | 1 of 1 run (re-run 3x during development, byte-identical each time) |
| F11-AC2 | `bun test .../census.test.ts` | `82 pass`, `0 fail`, `354 expect() calls` | 82 of 82 tests pass, 0 fail (re-run twice, identical) |
| F11-AC3 | `bun test .../colour-law.test.ts` | `SCANNED: 38 files`; `3 pass`, `1 fail` -- `export/AppliedBranding.tsx:43 -- text-white` | 3 of 4 tests pass, 1 fail (re-run twice, byte-identical both times) |
| F11-AC4 | `node scripts/ui-smoke.mjs investor-reporting ... --fixtures fe-s-10-global.json` | `LOC: /investor-reporting`, `rc=0` | N/A -- single capture; 4 of 4 fixtures matched (re-run twice, identical) |
| F11-AC5 | `... --fixtures fe-s-6-ready.json --click Analysis` | `rc=0`; PNG is the portal's generic error boundary, not the Analysis tab -- `CONSOLE[error]: Maximum update depth exceeded` (surprise `IRPT_FNTEND-W1-S12`) | N/A -- single capture; mechanical bar (`rc=0`) met (re-run twice, byte-identical crash both times) |
| F11-AC6 | `... --fixtures fe-s-7-smartx.json --click Holdings` | `rc=0`; same crash/PNG as AC5 | N/A -- single capture; mechanical bar met (re-run twice, identical) |
| F11-AC7 | `... --fixtures fe-s-9-modal.json --click Export` | `rc=0`; same crash/PNG as AC5 | N/A -- single capture; mechanical bar met (re-run twice, identical) |
| F11-AC8 | `... investor-reporting/print?bundle=... --fixtures fe-s-8-narrative.json` | `rc=0`; PNG: "cannot render reportKind 'performance-report': rev-000401 is absent" (a bundle-not-renderable message, not a crash; `?bundle=` triggers the already-known `DID NOT LAND` LOC print, per the WORKER FACE's own note) | N/A -- single capture; 1 of 1 fixture matched (re-run twice, identical) |
| F11-AC9 | judgment; N/A | the census, the brand review and all five PNGs (three of which are the portal's error boundary) are the record | N/A -- judgment criterion |

## F11-AC3's ONE genuine failure

`export/AppliedBranding.tsx` (itself never mounted anywhere -- see below) renders
`<span className="font-medium text-white">{label}</span>` with no same-file `<Panel>`/`variant="dark"`
ancestor and no `bg-*` utility anywhere in its own file. The scan's two extensions beyond the WORKER
FACE's literal wording (a self-contained dark background on the SAME class string; a Tailwind
state-variant prefix) were verified NOT to matter for this one violation -- neither anchor applies to
it -- and were verified TO matter for every other `text-white` occurrence in the tree
(`export/ExportButton.tsx`, `export/ExportModal.tsx`, `header/ClientSearch.tsx`,
`header/FirmDropdown.tsx`, `tabs/StatusPanel.tsx`, `tabs/analysis/InputReview.tsx`,
`tabs/reporting/PeriodControls.tsx`), all of which are documented, intentional, self-contained
coloured buttons/badges (`tabs/StatusPanel.tsx`'s own header: "every button on it is a solid,
dark-on-white indigo tile") that a literal-only scan would ALSO have flagged as false positives.
This scan's own two positive controls (`export/ExportButton.tsx` and `export/ExportModal.tsx` are
asserted NOT flagged) fired correctly both runs. This is a real, disclosed design-conformity gap, not
a test-authoring defect; recorded as surprise `IRPT_FNTEND-W1-S11`, `hazard_standing: ARMED`,
`disarm_owner: 3.0.0_SA_CVO`.

## The one-firm-catalogue crash (F11-AC5/AC6/AC7)

All three fixtures this order's own WORKER FACE names for the Analysis tab, Holdings tab and export
modal captures crash the whole `/investor-reporting` page (React "Maximum update depth exceeded",
caught by the app's error boundary) BEFORE any tab or modal content renders -- reproduced with and
without `--click`. Isolated by a clean discriminator: every fixture whose `resolve-scope` response
carries exactly ONE `permittedFirms` entry crashes (`fe-s-6-ready.json`, `fe-s-7-smartx.json`,
`fe-s-9-modal.json`, 3 of 3); every fixture with two entries does not (`fe-s-10-global.json`,
`fe-s-2-default.json`, 2 of 2). `global/useFirmContext.ts` is the only code path the codebase's own
comments name as engaging for a one-firm catalogue, and its own effect comment names the exact risk
this crash matches. This order writes no portal code and `global/useFirmContext.ts` is outside this
order's `<paths>`; recorded as surprise `IRPT_FNTEND-W1-S12`, `hazard_standing: ARMED` (a real
advisor session with one permitted firm would hit this today), `disarm_owner: 3.0.0_SA_CVO`.

## Determinism

Every criterion invocation was run at least twice: `census.ts` (5 runs total across development plus
2 final confirmation runs, output byte-identical after the last fix); `census.test.ts` and
`colour-law.test.ts` (2 runs each, identical pass/fail counts and identical violation list); all five
ui-smoke captures (2 runs each, identical `rc`, identical `LOC`, identical console/error output,
identical fixture-match counts).

## Mutant

No portal code is edited by this order, so there is no assertion of this order's OWN to mutate in the
usual sense; the mutant control instead targets `colour-law.test.ts`'s own detection logic, since a
scan that can never fire is a constant wearing a measurement's clothes. Mutation: temporarily widened
`LIGHT_ON_CANVAS_TOKEN` to also match `text-slate-900` (a colour every screen legitimately uses) with
the anchor logic unchanged. Expected: a flood of new false-positive violations across files with no
Panel/dark-bg/variant anchor. Observed: yes -- the "zero violations" test still reads `3 pass, 1 fail`
(one test, one assertion), but its failure diff grew from 1 violation to 28, adding **27 new**
`text-slate-900` violations across files with no dark anchor (`header/ScopeSummary.tsx`,
`tabs/StatusPanel.tsx`, `tabs/reporting/PeriodControls.tsx`, etc.) -- confirming the scan's
positive-firing path is live and its anchors are what keep the REAL run at exactly one violation
rather than the pattern being unreachable to fire at all. Reverted (`diff` against a pre-mutation
copy: no output, REVERT-CLEAN); re-ran `colour-law.test.ts` -- identical `3 pass, 1 fail` (the one
real `AppliedBranding.tsx` violation only) as before the mutation.

## Declared exclusions

- **An analysis-print capture** (`brand-review.md`'s "print, analysis" row): F11-AC8 names exactly one
  print invocation, using a PERFORMANCE bundle (`?bundle=perf-narrative-fixture-1`); no analysis-print
  fixture or route is named by this order's acceptance battery. The brand review cites FE-s-4's own
  earlier `fe-s-4_print_analysis_1440.png` for that content instead of fabricating a new capture this
  order was never asked to take.
- **Re-verifying `brand.tokens.json` against `deck_generation/brand_spec/brand.json`**: impossible from
  any worktree (the source is gitignored everywhere but the primary checkout) -- named as INERT-but-
  unverifiable already by `IRPT_FNTEND-W2-S1`'s own notes; not re-attempted here.

## Surprises

- `IRPT_FNTEND-W1-S11`: two FE-s-9 export components (`AppliedBranding.tsx`, `ReceiptPanel.tsx`) are
  never imported anywhere under the tree or `App.tsx`; `AppliedBranding.tsx`'s own light text has no
  dark anchor, and `colour-law.test.ts` (F11-AC3) genuinely fails on it. `hazard_standing: ARMED`,
  `disarm_owner: 3.0.0_SA_CVO`.
- `IRPT_FNTEND-W1-S12`: F11-AC5/AC6/AC7's own named fixtures each crash the whole page with "Maximum
  update depth exceeded" whenever the resolved scope carries exactly one permitted firm -- isolated to
  `global/useFirmContext.ts`, outside this order's `<paths>`. `hazard_standing: ARMED`,
  `disarm_owner: 3.0.0_SA_CVO`.
