# DSGN_RBNDV2 -- round 6 close run: the border-white sweep, the footer source casing, and a typecheck correction (RB6Y1-AC3, RB6Y2-AC3; RV-y-3 direct act)

**Author:** `2.0.0_SA_COO~RB`, 2026-10-15 ~17:3xZ. **Branch read:** `feature/dsgn-rbndv2-light` @3509eae8 (LOCAL, never pushed), dev build at port 5174, against the real backend. Method as in the round-5 record (the scratch walker copy with a JSON step file; armed, one load, disarmed; the login after disarm REFUSED each time).

## Correction of my own earlier claim (typecheck)

The merge-time typecheck I printed in the round-4 and round-5 close records (`tsc --noEmit -p .`, rc=0) was an EMPTY check: the portal's root `tsconfig.json` holds only project references and lists no source file, so tsc checked nothing. The instrument that covers the application and its tests is `tsc -p tsconfig.app.json --noEmit` (or `tsc -b`). Run with it at the round-6 drain, it reported `TS2769` in `src/__tests__/dsgn-rbndv2/rb-5-x5.hover-resolve.test.ts:30` (`maxBuffer` is not a known option of the `execSync` type), a defect that had been merged in round 5 under my "typecheck rc=0". It is repaired by `RV-y-3` (below). At the tip `3509eae8` the real typecheck reads rc=0 over the whole application and every design test. The earlier "0 errors" lines in the round-4 and round-5 records name an empty check and are withdrawn; the round-4 and round-5 portal changes are now covered by the rc=0 at this tip.

## Drain (merge-time checks, with the real typecheck)

| order | worker | proof (re-run in its worktree before the merge) | portal merge | workspace merge |
|---|---|---|---|---|
| RV-y-1 border-white class sweep | ~19 | VALID | 86db3d1b | 797ce8c192 |
| RV-y-3 (direct act) design tests typecheck and stand alone | ~21 | VALID | 5af00d94 | 34de367928 |
| RV-y-2 footer source casing | ~20 | VALID | 3509eae8 | f5116fb58d |

At the last portal merge, in the portal-only checkout (no workspace above it): `tsc -p tsconfig.app.json --noEmit` rc=0; `src/__tests__/dsgn-rbndv2` 27 pass 0 fail (14 files); panels, modal and market-performance test folders 18 pass 0 fail; eslint rc=0 on the touched folders. Every diff reviewed: 0 non-ASCII bytes added. Worktrees and worker branches removed; nothing pushed.

## RV-y-1 -- the border sweep (the CTO's item 1)

- Before and after list: `BORDER_SWEEP_LIST.md` (63 `border-white/N` classes in the 6 in-scope files before; 43 after: 20 DROP rows, 43 KEEP rows, each with tag, role and snippet; also a copy at `portal/src/__tests__/dsgn-rbndv2/fixtures/border-sweep-list.md`).
- Live walk of `/market`, Trending Topics rows (six rows read): BEFORE (taken at 16:26Z) each row `border-top-width 1px`, `border-top-color rgb(227, 231, 239)`; AFTER (17:00Z) each row `1px`, `rgba(0, 0, 0, 0)` (class `border-transparent`). The period chips (`1Q`, `YTD`, `1Y`) read `border-top-width 0px` (they never carried a box border; the active `90D` reads 0px), the dropdown controls were not part of the Market Overview panel read and stay under KEEP in the list.

## RV-y-2 -- footer source casing (the CTO's item 2)

77 footer string literals swept, 3 changed (`Source: Global News.` in `SentimentGauge.tsx`, `Source: Financial News.` twice in `ExecutiveSummary.tsx`); the test fails the suite on a lower-case source name in any non-test `.ts` or `.tsx` file. Live footers on `/market`: "October 15th, 2026, 7:18a ET | Source: Global News.", "... | Source: Bloomberg, CNBC, Financial Times, and more.", "... | Source: CNN." Worker rows `W20-S2` and `W20-S3` (lower-case qualifiers after a comma such as ", as of" and lower-case prose in a few literals) are not source names; the rule was applied to source-name segments only. `ExecutiveSummary.tsx:268` passes the data's own source names through `formatSourcesForFootnote` unchanged (row `W20-S1`): the live footer reads proper case today because the data names are proper case.

## RV-y-3 -- the repair (direct act)

The x5 test typechecks (no `maxBuffer`); the y1 test reads its list from a portal fixture and passes in the portal-only checkout (it failed three arms there before); a new test (`rb-6-y3.standalone.test.ts`) fails if any design test names a workspace path or `maxBuffer`.

## Carried, not cut

- Item 3 of the CTO's analysis: Andrew's next page's comments and the answer to `002b` (tooltip placement); FWD-4 (heat maps): his answer, owed at this terminal.
- 622 `border-white/N` occurrences in 119 files portal-wide; the Market Overview scope is swept, the other pages follow Andrew's walk.
- Surprise rows: all OBSERVATION and INERT (`W19-S1..S3`, `W20-S1..S4`, `W21-S1..S2`).
