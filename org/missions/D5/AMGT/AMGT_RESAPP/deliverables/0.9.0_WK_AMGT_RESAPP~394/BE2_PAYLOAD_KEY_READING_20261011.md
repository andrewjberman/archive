# AMGT-be-2 -- which portal build reads which Thesis payload key (round 98, read only)

Question: does the DEV build (`origin/DEV`) or the PROD-built page (`origin/PROD`) of the nested portal repository read the top-level key `fiscal_year_figures`, the model-block key `model.fiscal_year_figures`, or `check_face` from the `/thesis` payload? This reading drops nothing and writes nothing. A removal is not part of this order.

Method: two detached worktrees of the nested portal repository, outside the workspace (`C:/dev/scratch-be2-dev` and `C:/dev/scratch-be2-prod`), swept with native Glob and native Grep. Every site was read and classified in words. Counted sites are reads of the served payload only. Types, comments and fixtures are named and not counted.

## Sources

- origin/DEV 44ec7e70a97476fdafc8620beae4d2bfbdc41101 of the nested portal repository, detached worktree C:/dev/scratch-be2-dev, tree src/, tool native Glob `**/*.{ts,tsx}` then native Grep (ripgrep) for `fiscal_year_figures`, `check_face` and `team_sheet`: n=1157 .ts and .tsx files scanned.
- origin/PROD 37aa1247ee4ba487e5610dc5b78d65ae28468a99 of the nested portal repository, detached worktree C:/dev/scratch-be2-prod, same tree, same tools, same patterns: n=1124 .ts and .tsx files scanned.
- Whole-tree file sweep of both worktrees (no glob, native Grep, files with matches) for the three key names: n=18 files in origin/DEV and n=18 files in origin/PROD, all under src/pages/SecurityAnalysis (5 .ts and .tsx files, 13 fixture and harness files: .json, .cjs, .mjs). No file outside src/ names any of the three keys.

## Keys

KEY: fiscal_year_figures | DEV: 4 site(s) ModelTab.tsx:593 (top-level read: data.fiscal_year_figures, the ThesisBundle argument of buildModelSheet in ModelBody), ModelTab.tsx:602 (top-level read: data.fiscal_year_figures in the history sheet), CardFooter.tsx:188 (top-level read: string path fiscal_year_figures[].source walked by footerFor.model, live at ModelTab.tsx:897), postureCites.ts:369 (top-level read: thesis.fiscal_year_figures, where side.thesis is the served bundle handed over at PostureTab.tsx:663 and :671). Not counted: CardFooter.tsx:192 (top-level path inside whatChangedSources, a definition with no caller in either build), types.ts:1286 (type declaration), ModelTab.tsx:21 and figureIdentity.ts:22 (comments) | PROD: 4 site(s) ModelTab.tsx:543 (top-level read, ModelBody buildModelSheet argument), ModelTab.tsx:550 (top-level read, history sheet), CardFooter.tsx:188 (top-level read: string path fiscal_year_figures[].source walked by footerFor.model, live at ModelTab.tsx:815), postureCites.ts:369 (top-level read, same served bundle path as DEV). Not counted: CardFooter.tsx:192 (same uncalled definition as DEV), types.ts:1261 (type declaration), ModelTab.tsx:21 and figureIdentity.ts:22 (comments).

KEY: model.fiscal_year_figures | DEV: 2 site(s) CardFooter.tsx:187 (model-block read: string path model.fiscal_year_figures[].vintage walked by values() on the top-level bundle, so data.model.fiscal_year_figures feeding the footer time, live at ModelTab.tsx:897), CardFooter.tsx:188 (model-block read: string path model.fiscal_year_figures[].source feeding the footer sources, live the same way). No property access, destructure or local alias of model.fiscal_year_figures exists in src/. ThesisModelBlock (types.ts:1129) declares no fiscal_year_figures field. Not counted: none | PROD: 2 site(s) CardFooter.tsx:187 (model-block read: same string path, live at ModelTab.tsx:815), CardFooter.tsx:188 (model-block read: same string path, live the same way). ThesisModelBlock (types.ts:1124) declares no fiscal_year_figures field.

KEY: check_face | DEV: 6 site(s) ModelTab.tsx:523 (top-level read: data.check_face in ModelSummary), ModelTab.tsx:553 (top-level read: data.check_face passed as checks to SheetCellView in ModelBody), ModelTab.tsx:611 (top-level read: data.check_face in rowRefusal, ModelBody), ModelTab.tsx:617 (top-level read, same), ModelTab.tsx:692 (top-level read: rowRefusal in ModelBody), ModelTab.tsx:718 (top-level read: checks prop to SheetCellView in ModelBody). Not counted: types.ts:1287 (type declaration), types.ts:17 and ModelTab.tsx:21 (comments) | PROD: 6 site(s) ModelTab.tsx:473 (top-level read: data.check_face in ModelSummary), ModelTab.tsx:503 (top-level read: checks prop to ModelCell in ModelSummary), ModelTab.tsx:558 (top-level read: rowRefusal in ModelBody), ModelTab.tsx:564 (top-level read, same), ModelTab.tsx:624 (top-level read: rowRefusal in ModelBody), ModelTab.tsx:636 (top-level read: checks prop to ModelCell in ModelBody). Not counted: types.ts:1262 (type declaration), types.ts:17 and ModelTab.tsx:21 (comments).

## Census

DEV files scanned n=1157 (origin/DEV src/, .ts and .tsx, native Glob)
PROD files scanned n=1124 (origin/PROD src/, .ts and .tsx, native Glob)
matched n=34 (DEV 17 matching lines and PROD 17 matching lines, .ts and .tsx, for the two keys fiscal_year_figures and check_face; comments and type declarations are in the match count and excluded from the reads above; the 5 files are types.ts, ModelTab.tsx, CardFooter.tsx, postureCites.ts and figureIdentity.ts in each build)

## Control

CONTROL: team_sheet | DEV: 2 | PROD: 0 (the sweep run on team_sheet over the same src/ trees: origin/DEV reads at ModelTab.tsx:599 and :601 (data.model?.team_sheet), plus one type declaration at types.ts:1139 not counted; origin/PROD has no match in any file of src/. The sweep sees a read and distinguishes the two builds, reproducing round 46's reading.)

## Surfaces

READ: origin/DEV src/ .ts and .tsx, all 1157 files (native Glob and native Grep, full sweep)
READ: origin/PROD src/ .ts and .tsx, all 1124 files (native Glob and native Grep, full sweep)
READ: the 13 non-.ts src/ files named by the whole-tree sweep, all under src/pages/SecurityAnalysis/__harness__ (fixture JSON, harness CJS and MJS), listed and classed as test or fixture data, not served-build reads
READ: the footer walk on both builds (CardFooter.tsx values(), read() and footerFor.model, called from ModelTab.tsx)
READ: the posture cite resolver on both builds (postureCites.ts resolveCite, called from PostureTab.tsx)
NOT READ: built bundles (the minified JavaScript a build emits) of origin/DEV and origin/PROD. No build was run (no bun, npm or pip install), and no dist artifact exists in either worktree. Property names inside a bundle are not read, so a property access built at runtime is not checked here.
NOT READ: the Thesis route server that emits the /thesis payload, which lives outside the portal repository. The served key set is AMGT_CORPUS's measurement and is not re-read here.
NOT READ: print and PDF renderers outside src/. The whole-tree sweep found no file outside src/ naming the keys, but any server-side renderer is not read.
NOT READ: other API clients outside the portal repository (mcportal, opal_ai, dry_portal_vite). Inside the portal, no lib/research/api path exists under src/ (native Glob `**/research/api*` over origin/DEV src/ returned no files), so no in-portal consumer of that name exists.

## Outcome

OUTCOME fiscal_year_figures: READ-BY-BOTH
OUTCOME model.fiscal_year_figures: READ-BY-BOTH
OUTCOME check_face: READ-BY-BOTH

## Not changed

WRITES: none. No key is removed or edited, and this reading drops nothing. The scratch worktrees C:/dev/scratch-be2-dev and C:/dev/scratch-be2-prod are removed after reading. No push, no API, AWS or Bloomberg call.
