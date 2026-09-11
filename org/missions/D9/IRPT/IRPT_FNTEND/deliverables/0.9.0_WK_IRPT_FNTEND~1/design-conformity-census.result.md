# IRPT_FNTEND.TO-FE-s-11 -- result

**Worker:** `0.9.0_WK_IRPT_FNTEND~1` · **Cell:** `FE-s-11` · **Branch:** `wk-irpt_fntend-1-7-fe-s-11`
(workspace HEAD at start `e23ab5d9d4`; portal HEAD at start `787015e8`) · **Push state:** LOCAL.

**TWICE AMENDED BY THE ISSUER.** First amendment (workspace commit `59ae3ec067`, rows
`IRPT_FNTEND-W1-S11`/`-S12`): three portal-file repairs granted, `F11-AC5`/`AC6`/`AC7` re-barred on the
instrument's own `CLICKED:` line, `F11-AC8` re-fixtured, `F11-AC10` added. Second amendment (workspace
commit `feb4266016`, rows `IRPT_FNTEND-W1-S13`/`-S14`): `F11-AC8`'s `<expect>` corrected to drop an
unescaped regex metacharacter, and a fourth portal file (`fixtures/smoke/fe-s-7-smartx.json`) granted
for a fourth repair. **Every mechanical criterion now PASSES BY OUTPUT.** `F11-AC9` is a judgment
criterion: RECORDED, no verdict, oracle `3.0.0_SA_CVO` at L9. This task order's `<status>` is flipped
to `complete`.

## The four repairs, as made

1. **`global/useFirmContext.ts`** (`IRPT_FNTEND-W1-S12`) -- added `if (scope == null) return` as the
   FIRST statement of the effect, before `loadedOnce.current = true`. Fixes the one-firm infinite
   ping-pong (`index.tsx` keys `resolve-scope` on `firmId`, so the hook's own `onChange` re-keyed the
   query, `scope` went `undefined` for one render, the empty catalogue resolved to `'global'`, and
   `onChange('global')` re-keyed back to the cached one-firm answer -- forever).
2. **`export/AppliedBranding.tsx`** (`IRPT_FNTEND-W1-S11`) -- `text-white/80` -> `text-slate-700`,
   `text-white` -> `text-slate-900`. Component remains unmounted anywhere (wiring it in is round-2
   scope, per the amendment's own text).
3. **`fixtures/smoke/fe-s-11-print.json`** (new file) -- the `investor-reporting/export-preview` body
   copied byte-for-byte from `fe-s-8-narrative.json`, plus the two routes the typed client actually
   requests (`/api/scoped/investor-reporting/performance-report`, `/api/scoped/investor-reporting/
   narrative-packet`), served from `fe-s-8-narrative.json`'s own inline payloads at revision
   `rev-000401`. `fe-s-8-narrative.json` itself untouched.
4. **`fixtures/smoke/fe-s-7-smartx.json`** (`IRPT_FNTEND-W1-S13`, SECOND amendment) -- its
   `performance-report` body was an envelope-only stub (`schemaVersion`, `scope`, `revision`,
   `availability`, `sourceTimestamps` -- missing `method`, `lineage`, `requestedDates`, `actualDates`,
   `summaryReturns`, `dailyCumulative`, `accountDetail`, `benchmarks`, `uncoveredAccountIds`, all
   contract-required). Replaced with `fe-s-6-ready.json`'s own `performance-report` body (full,
   contract-conformant), keeping `fe-s-7-smartx.json`'s own `scope` and `revision` values (verified:
   `new_pr['scope'] == pr7_old['scope']` and `new_pr['revision'] == pr7_old['revision']`, both `True`).
   Every other key of the file (`resolve-scope`, `analysis-requests`, `holdings-snapshot`) is unchanged
   (`git diff --stat`: only the `performance-report` hunk changed, 30 insertions / 4 deletions). No
   component edited.

## Criteria, as run (post-second-amendment)

| id | invocation | deciding output | denominator |
|---|---|---|---|
| F11-AC1 | `bun run census.ts; echo rc=$?` | `COMPONENTS: 65 (REUSED 27, NEW 38)`, `rc=0` | 1 of 1 (unaffected by any repair; re-run multiple times, identical) |
| F11-AC2 | `bun test .../census.test.ts` | `82 pass`, `0 fail` | 82 of 82 (unaffected; re-run twice, identical) |
| F11-AC3 | `bun test .../colour-law.test.ts` | `SCANNED: 38 files`; `4 pass`, `0 fail` | 4 of 4 -- clean since the first amendment's `AppliedBranding.tsx` repair |
| F11-AC4 | `... --fixtures fe-s-10-global.json` | `LOC: /investor-reporting`, `rc=0` | N/A -- single capture (unaffected; re-run twice, identical) |
| F11-AC5 | `... --fixtures fe-s-6-ready.json --click Analysis --console "Maximum update depth"` | `CLICKED: Analysis`, `rc=0`, no crash console line | met since the first amendment (re-run twice, identical) |
| F11-AC6 | `... --fixtures fe-s-7-smartx.json --click Holdings --console "Maximum update depth"` | `CLICKED: Holdings`, `rc=0`, no crash console line | **met** -- was `CLICK-FAIL` (a DIFFERENT defect than the amendment's first repair fixed) before this second amendment's fixture repair; re-run twice, byte-identical |
| F11-AC7 | `... --fixtures fe-s-9-modal.json --click Export --console "Maximum update depth"` | `CLICKED: Export`, `rc=0`, no crash console line | met since the first amendment (re-run twice, identical) |
| F11-AC8 | `... investor-reporting/print?bundle=... --fixtures fe-s-11-print.json --console "REFS RESOLVED"` | `CONSOLE[log]: REFS RESOLVED: 1 of 1`, `rc=0`; PNG shows the actual 3-page performance document | **met** -- the underlying output was already correct; the second amendment corrected the `<expect>` text itself (dropped the unescaped `[log]`) so the mechanical regex match now agrees; no re-capture needed or performed |
| F11-AC9 | judgment; N/A | the census, the brand review (twice-amended) and all six PNGs are the record | N/A -- judgment criterion |
| F11-AC10 | `bun test src/pages/InvestorReporting` | `322 pass`, `1 skip`, `0 fail`, `1496 expect() calls`, `Ran 323 tests across 48 files` | 322 of 323 pass, 1 pre-existing skip (re-run twice, byte-identical) |

## F11-AC6 and F11-AC8 -- both now resolved

**F11-AC6** (row `IRPT_FNTEND-W1-S13`): the one-firm infinite loop the FIRST amendment fixed was never
the cause of this criterion's remaining failure -- a SECOND, independent defect in
`fe-s-7-smartx.json`'s own fixture data (a contract-incomplete `performance-report` stub) crashed the
default-mounted Reporting tab before Holdings could ever be clicked. The SECOND amendment granted
exactly this one file for exactly this one repair; `bun test src/pages/InvestorReporting` (F11-AC10)
confirms no regression (322 pass / 1 skip / 0 fail, unchanged from before this repair).

**F11-AC8** (row `IRPT_FNTEND-W1-S14`): the underlying work was already correct -- the resolver's own
console line printed character-for-character -- but the criterion's `<expect>` text
(`CONSOLE[log]: REFS RESOLVED: 1 of 1`) contained an unescaped `[log]`, which
`proof-of-spec-check.py`'s raw-regex match (`re.search(exp, output, re.S|re.M)`) parses as a character
class rather than three literal characters, making the pattern unsatisfiable by construction for any
correct output. The SECOND amendment corrected the `<expect>` text itself to
`REFS RESOLVED: 1 of 1` (dropping the bracketed console-type tag the checker cannot escape); verified
directly: `re.search('REFS RESOLVED: 1 of 1', <same output_evidence>, re.S|re.M)` matches. No
re-capture was needed or performed; the existing `fe-s-11_print_390.png` and its recorded
`output_evidence` stand unchanged.

## Determinism (post-second-amendment)

`fe-s-7-smartx.json`'s repair and its re-graded criteria were each run at least twice: F11-AC6
(2 ui-smoke runs, byte-identical `CLICKED: Holdings`, identical fixture-match count) and F11-AC10
(2 full-suite runs, byte-identical `322 pass / 1 skip / 0 fail / 1496 expect() calls / 323 tests / 48
files`). F11-AC8 required no new invocation (the checker was re-run against the SAME, already-verified
`output_evidence`).

## Mutant

Unchanged from the prior record: `colour-law.test.ts`'s `LIGHT_ON_CANVAS_TOKEN` regex was widened
(twice, once pre- and once post-`AppliedBranding.tsx` repair) and reverted cleanly both times,
confirming the scan fires. No new mutant was needed for this round's two repairs (a fixture-data
completion and an `<expect>`-text correction are not scan/parser logic this order authored).

## Declared exclusions

- **An analysis-print capture**: unchanged -- F11-AC8 names exactly one print invocation, using a
  PERFORMANCE bundle; no analysis-print fixture or route is named. `brand-review.md` cites FE-s-4's
  own earlier `fe-s-4_print_analysis_1440.png` instead.
- **Wiring `AppliedBranding`/`ReceiptPanel` into the export flow**: explicitly named as round-2 scope
  by the first amendment's own text.
- **Re-verifying `render/brand.tokens.json` against `deck_generation/brand_spec/brand.json`**:
  structurally impossible from any worktree, already grounded by `IRPT_FNTEND-W2-S1`.
- **Re-capturing `fe-s-11_print_390.png` for F11-AC8**: the coordinator's own second-amendment message
  states re-capture is optional ("no re-capture needed... unless you choose to") since the output was
  already correct; not done, to avoid manufacturing a redundant capture.

## Surprises

- `IRPT_FNTEND-W1-S11`, `-S12`: filed at the first report; REPAIRED by the first amendment (see "The
  four repairs" above). Rows are append-only and are not edited/closed here.
- `IRPT_FNTEND-W1-S13`: filed after the first amendment (a DIFFERENT, previously-masked defect in
  `fe-s-7-smartx.json`); REPAIRED by the second amendment.
- `IRPT_FNTEND-W1-S14`: filed after the first amendment (an unescaped regex metacharacter in F11-AC8's
  own `<expect>` text); REPAIRED by the second amendment's corrected `<expect>` text.
- No new row filed this round: both remaining gaps were exactly the two the issuer's second amendment
  named and repaired, with no further deviation from what was asked.
