# Session log -- `0.9.0_WK_AMGT_RESAPP~132` on `AMGT-rl-3`

Worktree `C:/tmp/wk-amgt-37-132`, branch `wk-AMGT_RESAPP-132`; nested portal worktree
`C:/tmp/wk-amgt-37-132/portal`, branch `wk-AMGT_RESAPP-132-portal`.

## Preflight
- `git rev-parse --abbrev-ref HEAD` -> `wk-AMGT_RESAPP-132`
- `git rev-parse --show-toplevel` -> `C:/tmp/wk-amgt-37-132`
- `test -d org && test -d .tools && echo TREE-OK` -> `TREE-OK`
- `test -f portal/scripts/ui-class-census.mjs && echo INSTRUMENT-OK` -> `INSTRUMENT-OK`

## What was read before writing
- `tabs/ThesisTab.tsx`, `components/ThesisDriverChart.tsx` (prior cut, AMGT-rj-2/rj-9 era)
- `__harness__/drafting.harness.cjs`, `__harness__/tabs.harness.cjs` (read-only reference for
  cross-cutting markup conventions this cell must not break)
- `types.ts` (`DraftedSection`, `DraftedSentence`, `DraftedEvidence`, `DriverChart`,
  `ThesisBundle`, `DraftingProvenance`, `DraftingSource`)
- `components/CheckFaceBadge.tsx`, `IdentityLine.tsx`, `ProvenanceLine.tsx`,
  `GenerationCaption.tsx` (read-only; NOT restyled; `ProvenanceLine`/`GenerationCaption` do not
  fit the Thesis bundle's shape and are not used by this file, same as the prior cut)
- `DESIGN.md` (typography ladder: label 13px/700, body 16px/400, footnote 11px/400; C3 surface
  roles; C12 states) and `src/ui/components/states/{PanelStates.tsx,cause.ts,index.ts}`,
  `src/ui/components/panels/Panel.tsx` (`nested` variant resolves to the white surface, no
  `dark-band`)
- `scripts/ui-class-census.mjs` (the exact regexes AC2 grades against) and the two fixtures
  (`thesisBundle.drafted.BA_US_Equity.json`: SERVED, 5 sections, 4 non-empty -- 9/10/9/0/10
  sentences on company_description/investment_thesis/risks/ceo_bio/recommendation, 38 total,
  all PASS, 48 evidence records, thesis_driver_chart key absent -> ABSENT branch;
  `thesisBundle.BABA_US_Equity.json`: an older capture with no `drafting_status` field and an
  empty `drafted_sections` array at all -- used as the constructed second render)

## Key design decisions (worker authority; not a surprise -- within the cell's own bounds)
- **Marker discipline is the hard constraint.** `drafting.harness.cjs`'s own `sentences` array
  is built by iterating `bundle.drafted_sections` in the FIXTURE's own array order
  (company_description, investment_thesis, risks, ceo_bio, recommendation) and requires
  `data-drafted-sentence="0..37"` to appear in the HTML in strictly increasing byte position.
  That fixes the marked-sentence DOM order and cannot be reordered without breaking AC3. So
  "the recommendation first" is built as a SEPARATE, UNMARKED preview (the section's first
  sentence, plain text, no `data-drafted-sentence`, no face, no disclosure) placed before
  everything else; the FULL recommendation section, with its real markers and every sentence's
  face and evidence, still renders in the bundle's own order within the ladder below.
- **`sections_headed` = 4**, read off the fixture as "non-empty `drafted_sections` entries"
  (company_description, investment_thesis, risks, recommendation) -- company_description gets
  its own `data-thesis-section-heading` too (styled as a flowing summary paragraph, no 4px
  indigo top rule) so the count matches "the fixture's drafted sections with text" literally;
  only investment_thesis/risks/recommendation/ceo_bio(if text) also get the pillar-card 4px
  indigo top rule.
- **`disclosures`/`passages_in_dom`/`accession_lines`/`pass_faces_kept` all read off the
  fixture's own sentence/evidence counts (38/48/48/38)** -- the recommendation highlight
  preview carries NO `data-thesis-discloses`/face markers of its own, so nothing is
  double-counted between the preview and the full section.
- **Chart split:** neither fixture ever serves `thesis_driver_chart` SERVED, so
  `chart_split_or_absent_state` grades the ABSENT branch only: `data-thesis-chart-layout="full"`
  (never `"split"`) and the chart's own `PanelEmpty surface="panel"` card
  (`data-driver-chart="ABSENT"` + `data-panel-state="empty"`). `ThesisDriverChart.tsx`'s SERVED
  branch (40/60 split via `md:col-span-2`/`md:col-span-3`) is built and typechecks but is not
  exercised by either provided fixture -- named in the harness's own `limits` line.
- **Title-attribute check false positive, caught and fixed in-session.** A first cut of
  `title_attr_passages` used a bare substring search on `'title="'`, which also matched this
  harness's OWN instrumentation attribute (`data-panel-header-title="..."`, itself ending in
  `title="`) -- 2 false hits. Fixed with a negative-lookbehind regex
  (`/(?<![\w-])title="/g`) that only counts a standalone `title=` attribute; re-run confirmed
  0.

## Commands run (chronological, verbatim where load-bearing)
- `cd "$(git rev-parse --show-toplevel)/portal" && node scripts/ui-class-census.mjs
  src/pages/SecurityAnalysis/tabs/ThesisTab.tsx
  src/pages/SecurityAnalysis/components/ThesisDriverChart.tsx` -- BEFORE any edit:
  `idiom=7 size=5 ... total=12` (chart) / `idiom=13 size=3 weight=1 ... total=17` (tab),
  `FILES 2 TOTAL 29`
- `node node_modules/typescript/bin/tsc --noEmit -p tsconfig.json` -- rc=0, whole project,
  before AND after the rewrite (the `node_modules/.bin/tsc` wrapper script fails under this
  worktree's linked node_modules -- resolved by invoking `typescript/bin/tsc` directly)
- `node src/pages/SecurityAnalysis/__harness__/drafting.harness.cjs` -- CHECKS-OK 8 of 8,
  confirmed BEFORE touching `ThesisDriverChart.tsx` (chart is stubbed null in that harness) and
  AGAIN after the full rewrite of both files
- `node src/pages/SecurityAnalysis/__harness__/thesisLadder.harness.cjs` (new file) --
  CHECKS-OK 10 of 10 after the title-attribute fix above
- **Mutant control:** `sed -i` renamed `data-thesis-first="recommendation-highlight"` to
  `data-thesis-first-MUTATED=...` in `ThesisTab.tsx`, re-ran the harness -> ONLY
  `recommendation_first` flipped to `false` (`CHECKS-WRONG-WAY recommendation_first`), every
  other check unchanged; reverted from a byte-for-byte backup (`diff` confirmed
  `IDENTICAL-AFTER-REVERT`); re-ran -> CHECKS-OK 10 of 10 again.
- **Determinism control:** ran the new harness twice in a row, diffed the two JSON outputs with
  the volatile `"at":` timestamp line stripped -> byte-identical.
- `cd portal && bash ../.tools/safe-commit.sh --author "0.9.0_WK_AMGT_RESAPP~132
  <0.9.0_WK_AMGT_RESAPP~132@opal.agent>" -F <msgfile> -- tabs/ThesisTab.tsx
  components/ThesisDriverChart.tsx __harness__/drafting.harness.cjs
  __harness__/thesisLadder.harness.cjs` -> portal commit `3c863eea2549e1bf579f1c9764488d4416fe4de3`
  (4 files changed, 613 insertions, 162 deletions); commit-gate WARN is EXPECTED and named (it
  only reads `.py`/`.sh`/`.tf`/`org/projects/*.json`, none of which this commit touches --
  tsc + the two harnesses are the language-appropriate instruments, both run and cited above)
- Re-ran AC1/AC2/AC3 AT the committed portal HEAD (`git -C portal rev-parse HEAD` ==
  `3c863eea2549e1bf579f1c9764488d4416fe4de3`) -- all three unchanged (10 of 10 / FILES 2 TOTAL 0
  / 8 of 8).

## Declared exclusions
- Making the SERVED (40/60 split, real chart) branch of `ThesisDriverChart.tsx` exercised by a
  harness assertion: out of scope -- neither provided fixture (`thesisBundle.drafted.
  BA_US_Equity.json`, `thesisBundle.BABA_US_Equity.json`) ever serves `thesis_driver_chart`
  SERVED. The branch is built, typechecks, and is documented as unexercised in the harness's
  own `limits` line.
