# IRPT_FNTEND.TO-FE-s-11 -- result

**Worker:** `0.9.0_WK_IRPT_FNTEND~1` · **Cell:** `FE-s-11` · **Branch:** `wk-irpt_fntend-1-7-fe-s-11`
(workspace HEAD at start `e23ab5d9d4`; portal HEAD at start `787015e8`) · **Push state:** LOCAL.

**AMENDED BY THE ISSUER** at workspace commit `59ae3ec067` on rows `IRPT_FNTEND-W1-S11`/`-S12`:
`<paths>` gained three portal files for three named repairs; `F11-AC5`/`AC6`/`AC7` were re-barred
on the instrument's own printed `CLICKED:` line; `F11-AC8` was re-fixtured; `F11-AC10` (whole-suite
green) was added. **Every mechanical criterion now PASSES BY OUTPUT except F11-AC6**, which still
fails -- on a DIFFERENT, previously-masked defect the amendment did not name and this order's grant
does not cover (surprise `IRPT_FNTEND-W1-S13`). `F11-AC9` is a judgment criterion: RECORDED, no
verdict, oracle `3.0.0_SA_CVO` at L9. Because one mechanical criterion still fails, this task order's
`<status>` is **not** flipped to `complete`.

## The three repairs, as made

1. **`global/useFirmContext.ts`** (`IRPT_FNTEND-W1-S12`) -- added `if (scope == null) return` as the
   FIRST statement of the effect, before `loadedOnce.current = true`. No other line changed
   (`git diff`: 8 insertions, 0 deletions, all comment + the one guard line). Fixes the one-firm
   infinite ping-pong: `index.tsx` keys `resolve-scope` on `firmId`, so the hook's own `onChange`
   re-keyed the query, `scope` went `undefined` for one render, the empty catalogue resolved to
   `'global'`, and `onChange('global')` re-keyed back to the cached one-firm answer -- forever.
2. **`export/AppliedBranding.tsx`** (`IRPT_FNTEND-W1-S11`) -- `text-white/80` -> `text-slate-700`,
   `text-white` -> `text-slate-900`. Nothing else changed (`git diff`: 2 lines changed). The
   component is still never mounted anywhere (unchanged from before this amendment); wiring it in is
   explicitly out of scope per the amendment's own text.
3. **`fixtures/smoke/fe-s-11-print.json`** (new file) -- the `investor-reporting/export-preview` body
   copied byte-for-byte from `fe-s-8-narrative.json` (verified: `d['investor-reporting/export-preview']
   == orig[...]` is `True`), plus two new keys for the routes the typed client actually requests
   (`api/endpoints/investor-reporting.ts`'s `irRoute`: `/api/scoped/investor-reporting/performance-report`
   and `/api/scoped/investor-reporting/narrative-packet`, matching `fe-s-6-ready.json`'s full-path key
   shape), served from `fe-s-8-narrative.json`'s own inline `performanceReport`/`narrativePacket`
   payloads (the `performanceReport`'s `revision.revisionId` set to `rev-000401` to match the bundle's
   `reports[0].authorizedRevision`; `narrativePacket` unchanged -- it already carries
   `performanceRevision: "rev-000401"`). `fe-s-8-narrative.json` itself is untouched (`git diff --stat`:
   no output).

## Criteria, as run (post-amendment)

| id | invocation | deciding output | denominator |
|---|---|---|---|
| F11-AC1 | `bun run census.ts; echo rc=$?` | `COMPONENTS: 65 (REUSED 27, NEW 38)`, `rc=0` | 1 of 1 (unaffected by the repairs; re-run twice, identical) |
| F11-AC2 | `bun test .../census.test.ts` | `82 pass`, `0 fail` | 82 of 82 (re-run twice, identical) |
| F11-AC3 | `bun test .../colour-law.test.ts` | `SCANNED: 38 files`; `4 pass`, `0 fail` | 4 of 4 -- **now clean** (was 3/4 before the repair) |
| F11-AC4 | `... --fixtures fe-s-10-global.json` | `LOC: /investor-reporting`, `rc=0` | N/A -- single capture (re-run twice, identical) |
| F11-AC5 | `... --fixtures fe-s-6-ready.json --click Analysis --console "Maximum update depth"` | `CLICKED: Analysis`, `rc=0`, no crash console line | met (was `CLICK-FAIL`/crash before the repair; re-run twice, identical) |
| F11-AC6 | `... --fixtures fe-s-7-smartx.json --click Holdings --console "Maximum update depth"` | `CLICK-FAIL: Holdings`, `rc=0`; PNG is the error boundary; console shows a DIFFERENT error (`TypeError: Cannot read properties of undefined (reading 'currency')` at `ReportingTab.tsx:36`, not "Maximum update depth") | **NOT met** -- see below (re-run twice, byte-identical) |
| F11-AC7 | `... --fixtures fe-s-9-modal.json --click Export --console "Maximum update depth"` | `CLICKED: Export`, `rc=0`, no crash console line | met (was `CLICK-FAIL`/crash before the repair; re-run twice, identical) |
| F11-AC8 | `... investor-reporting/print?bundle=... --fixtures fe-s-11-print.json --console "REFS RESOLVED"` | `CONSOLE[log]: REFS RESOLVED: 1 of 1`, `rc=0`; PNG shows the actual 3-page performance document | met, 3 of 3 fixtures matched (re-run twice, identical) |
| F11-AC9 | judgment; N/A | the census, the brand review (amended) and all six PNGs are the record | N/A -- judgment criterion |
| F11-AC10 | `bun test src/pages/InvestorReporting` | `322 pass`, `1 skip`, `0 fail`, `1496 expect() calls`, `Ran 323 tests across 48 files` | 322 of 323 pass, 1 pre-existing skip (re-run twice, byte-identical) |

## F11-AC6's remaining failure -- a DIFFERENT defect, outside this order's grant

The repair fixed the infinite loop; it did not fix a SECOND, independent problem the loop had been
masking. `fe-s-7-smartx.json`'s own `investor-reporting/performance-report` fixture is a five-field
stub (`schemaVersion`, `scope`, `revision`, `availability`, `sourceTimestamps` -- no `method` field at
all), built for FE-s-7's own Holdings-focused smoke test. `tabs/reporting/ReportingTab.tsx:36`'s
`toRenderPerformanceReport` reads `report.method.currency` unconditionally, and the Reporting tab is
the DEFAULT-mounted tab -- so it throws (`TypeError: Cannot read properties of undefined (reading
'currency')`) on page load, before "Holdings" can ever be clicked. Isolated cleanly: F11-AC5's and
F11-AC7's own fixtures (`fe-s-6-ready.json`, `fe-s-9-modal.json`) both carry a full `method` object
and both now succeed under the identical post-repair code. `tabs/reporting/ReportingTab.tsx` is not
one of this order's three granted repair files (`global/useFirmContext.ts`, `export/AppliedBranding.tsx`,
`fixtures/smoke/fe-s-11-print.json`), so it is not edited here. Recorded as surprise
`IRPT_FNTEND-W1-S13`, `hazard_standing: INERT` (a fixture-authoring gap, not a shape any real
`resolve-scope`/`performance-report` pairing has been shown to produce), `disarm_owner:
3.0.0_SA_CVO`.

## Determinism (post-repair)

Every amended/re-run criterion invocation was run at least twice: `census.ts`, `census.test.ts`,
`colour-law.test.ts` and the full-suite `F11-AC10` run (2 runs each, byte-identical); all five
re-captured ui-smoke invocations (F11-AC4/5/6/7/8, 2 runs each, identical `rc`, identical printed
bars, identical fixture-match counts, identical console lines).

## Mutant (unchanged from the pre-amendment record; still valid)

`colour-law.test.ts`'s `LIGHT_ON_CANVAS_TOKEN` regex was temporarily widened to also match
`text-slate-900` (a colour every InvestorReporting screen legitimately uses -- including, now,
`AppliedBranding.tsx`'s own repaired token), with the anchor logic unchanged. Expected: a flood of
new false-positive violations. Observed: the "zero violations" assertion's failure diff grew from 0
(post-repair baseline) to 28 new `text-slate-900` violations across files with no dark anchor.
Reverted (`diff` against a pre-mutation copy: no output, REVERT-CLEAN); re-ran `colour-law.test.ts` --
identical `4 pass, 0 fail` as before the mutation. (Originally run pre-amendment against the
then-1-violation baseline with the same 27-new-violation result; re-verified here against the
now-0-violation baseline for completeness.)

## Declared exclusions

- **An analysis-print capture**: unchanged from the pre-amendment record -- F11-AC8 names exactly one
  print invocation, using a PERFORMANCE bundle; no analysis-print fixture or route is named.
  `brand-review.md` cites FE-s-4's own earlier `fe-s-4_print_analysis_1440.png` instead.
- **Fixing `tabs/reporting/ReportingTab.tsx`'s missing-`method` crash, or `fe-s-7-smartx.json`'s
  fixture shape**: outside this order's `<paths>` (the amendment names exactly three repair files,
  none of which is this one). Recorded as surprise `IRPT_FNTEND-W1-S13` rather than edited.
- **Wiring `AppliedBranding`/`ReceiptPanel` into the export flow**: explicitly named as round-2 scope
  by the amendment's own text ("NOT done here").
- **Re-verifying `render/brand.tokens.json` against `deck_generation/brand_spec/brand.json`**:
  unchanged from the pre-amendment record -- structurally impossible from any worktree, already
  grounded by `IRPT_FNTEND-W2-S1`.

## Surprises

- `IRPT_FNTEND-W1-S11` and `IRPT_FNTEND-W1-S12`: filed pre-amendment; both REPAIRED by this
  amendment (see "The three repairs" above). Rows are append-only and are not edited/closed here;
  the repair is recorded as a NEW fact in this result file and in the proof instance.
- `IRPT_FNTEND-W1-S13` (NEW): F11-AC6's own fixture (`fe-s-7-smartx.json`) crashes the DEFAULT
  Reporting tab on a missing `method` field in its `performance-report` stub -- a different,
  previously-masked defect in `tabs/reporting/ReportingTab.tsx`, outside this order's grant.
  `hazard_standing: INERT`, `disarm_owner: 3.0.0_SA_CVO`.
