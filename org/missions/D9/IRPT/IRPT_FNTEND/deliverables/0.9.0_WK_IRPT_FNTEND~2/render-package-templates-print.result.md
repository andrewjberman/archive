# IRPT_FNTEND.TO-FE-s-4 -- result

**Worker:** `0.9.0_WK_IRPT_FNTEND~2` · **Cell:** `FE-s-4` · **Branch:** `wk-irpt_fntend-2-1-fe-s-4`
(workspace HEAD at start `d1f613fff3`; portal HEAD at start `6b614a5a`) · **Push state:** LOCAL.

Every mechanical criterion PASSES BY OUTPUT. `F4-AC9` is a judgment criterion: its output is
RECORDED here and in the proof instance with NO verdict; the oracle is `3.0.0_SA_CVO` at L9.

## What was built

`portal/src/pages/InvestorReporting/render/` -- the versioned rendering package that BOTH the screen
preview and the server-side PDF render. 13 TypeScript sources (70,590 bytes), one stylesheet, three
render fixtures, the packaged brand tokens and logo, the font licence; plus two smoke maps and six
test files. Portal commit `7f6236cf` (29 files, 4,565 insertions).

- `manifest.ts` -- `RENDER_PACKAGE` (version, `supportedContracts`, templates, fonts, `pageOptions`)
  and `assertSupported`, which refuses an unlisted `schemaVersion` **per carried contract**, not only
  at the envelope, naming the package version and the refused version.
- `brand.ts` + `brand.tokens.json` -- hex verbatim from `deck_generation/brand_spec/brand.json`;
  CSS pixel and PDF point constants are separate, named, and never mixed.
- `print.css` -- named `@page` rules (letter landscape for performance, letter portrait for
  analysis), page-break rules, footer/footnote placement, three `@font-face` blocks.
- `performance/` -- Summary, CumulativeReturnChart, PeriodResults, AccountDetail, MethodsAndSources,
  Disclosures, PerformanceDocument (4 pages with a narrative, 3 without).
- `analysis/AnalysisDocument.tsx` -- certified sections in producer ordinal order, portrait, each
  value with its own as-of date, unit, currency and source coordinate; no narrative page.
- `PrintEntry.tsx` -- `/investor-reporting/print`, one bundle read through the typed client's
  export-preview operation, then `assertSupported`, then the template `bundle.reportKind` names.
- `App.tsx` -- exactly two inserted lines (lazy import, Route). `git diff`: 2 insertions, 0 deletions.

**The package computes nothing.** No return arithmetic, no gain from ending minus beginning, no
averaging, no missing value as zero: an unsupported metric renders the word `UNAVAILABLE` with the
reason the source gave. `fields.test.ts` asserts both halves.

## Criteria, as run

| id | invocation | deciding output | denominator |
|---|---|---|---|
| F4-AC1 | `bun run typecheck; echo rc=$?` | `rc=0` | 1 of 1 program (all 13 render sources + 6 test files) |
| F4-AC2 | `bun test .../determinism.test.ts` | `4 pass, 0 fail`; performance 17266 bytes twice, analysis 10314 bytes twice | 4 of 4 tests |
| F4-AC3 | `bun test .../manifest.test.ts` | `9 pass, 0 fail`; refusal names `investor-reporting/9` and the package version | 13 of 13 sources scanned; 4 of 4 contracts listed; 4 of 4 fixture versions resolved |
| F4-AC4 | `bun test .../fields.test.ts` | `5 pass, 0 fail`; `106 of 106` scalar leaves present | 19 of 19 top-level fields; 3 of 3 unsupported metrics render the word, 0 render a number |
| F4-AC5 | `bun test .../analysis-no-narrative.test.ts` | `4 pass, 0 fail`; analysis `0 period-in-context page(s)` | 0 of 3 analysis pages, 0 of 262 source lines; positive control 1 of 4 performance pages |
| F4-AC6 | `bun test .../determinism-bounds.test.ts` | `6 pass, 0 fail`; clock 0, randomness 0, locale 0, fetch outside PrintEntry 0 | 13 of 13 sources, 70590 bytes |
| F4-AC7 | `node scripts/ui-smoke.mjs "investor-reporting/print?bundle=perf-fixture-1" ...` | `rc=0`, `LOC : /investor-reporting/print`, `FIXTURES: 1 declared; 1 matched` | 1 of 1 capture |
| F4-AC8 | `node scripts/ui-smoke.mjs "investor-reporting/print?bundle=analysis-fixture-1" ...` | `rc=0`, `LOC : /investor-reporting/print`, `FIXTURES: 1 declared; 1 matched` | 1 of 1 capture |
| F4-AC9 | read the two PNGs | RECORDED, NO VERDICT -- see the instance's `output_evidence` | 2 of 2 captures |

**`LOC`, recorded as the criterion asks:** `/investor-reporting/print` on both captures. Both runs
also print `<-- DID NOT LAND (auth redirect? bad route?)`. That suffix is the INSTRUMENT, not the
route: `ui-smoke.mjs` compares `window.location.pathname` against the full route argument, which
carries `?bundle=...`, so the comparison cannot hold for any query-carrying route. The pages landed --
the rendered `TEXT` is the performance and analysis document respectively, the declared fixture matched,
and the PNGs carry three pages each. Filed as `IRPT_FNTEND-W2-S5`.

## Controls

- **MUTANT, fired.** `manifest.test.ts` takes the shipped performance fixture, sets
  `performanceReport.schemaVersion` to `investor-reporting/7`, and the gate refuses it by name --
  while the un-mutated fixtures in the same run are NOT refused, so the refusal is caused by the
  mutation and not by a gate that refuses everything.
- **DETERMINISM, stable.** Every criterion ran twice (once at authoring, once in a consecutive sweep
  after the last edit) with identical output, and the render itself is compared byte-for-byte inside
  F4-AC2 for both templates, including a re-parsed-bytes pair.
- **Positive controls** inside four of the five test files, because an empty string, a wrong path or a
  broken read reads exactly like a clean pass: markup length and a known id in F4-AC2; the
  gate-is-not-a-constant arm in F4-AC3; an absent token in F4-AC4; a present token in F4-AC6; and the
  narrative page rendered ON PURPOSE in F4-AC5.

## Surprise rows filed (5)

| id | class / hazard | one line |
|---|---|---|
| `IRPT_FNTEND-W2-S1` | OBSERVATION / INERT | The brand token file and the logo package are gitignored (`deck_generation/.gitignore:14-15`), so both are absent from every worktree; copied into the package from the primary checkout by absolute path. |
| `IRPT_FNTEND-W2-S2` | OBSERVATION / **ARMED** (`2.0.0_SA_COO~F`) | The FE-s-1 `ExportBundle` carries no `reportKind`, no payloads, no beginning/ending value and no disclosure text; the package defines an additive `RenderBundle`. A backend built to the contract as written would be refused, not rendered. |
| `IRPT_FNTEND-W2-S3` | OBSERVATION / **ARMED** (`2.0.0_SA_COO~F`) | No Lato binary exists anywhere reachable and fetching one is egress off Opal infrastructure, so the packaged fonts could not be packaged. Both acceptance PNGs therefore show the fallback face -- which is what F4-AC9 will be grading. |
| `IRPT_FNTEND-W2-S4` | OBSERVATION / **ARMED** (`2.0.0_SA_COO~F`) | recharts 3.7.0 renders an empty wrapper under `renderToStaticMarkup` (127 bytes, no SVG), so a server-side render without a browser layout would emit a chartless report. Mitigated in-package: endpoint labels and the full series table are real DOM. |
| `IRPT_FNTEND-W2-S5` | OBSERVATION / INERT | `ui-smoke.mjs` prints DID-NOT-LAND for every query-carrying route while landing correctly. |

## Declared exclusions

The Lato binaries (S3); verification of the packaged brand copies against their gitignored source
(S1); the period-in-context page's CONTENT (FE-s-8 owns it -- this cell owns the slot and the rule
that it exists only with a narrative packet); the server-side PDF renderer (a different surface); any
live backend read (the scoped routes do not exist yet -- IRPT_BCKEND B15 builds them, and both
captures ran entirely off checked-in fixtures with no live vendor call).

## Proof

`IRPT_FNTEND.TO-FE-s-4.render-package-templates-print.proof_of_spec.json`, validated with
`python .tools/proof-of-spec-check.py <instance> F4-AC1,...,F4-AC9` -- **`VALID (rc=0)`**,
`acceptance rows=9 | violations=0`, `surprises-frame: 5 entries; 5 open with a row id; 5 resolve to a
channel row`, alignment forward 9/9 and backward 1/1.
