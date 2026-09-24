# IRPT_FNTEND.TO-FE-s-80 -- result

**Worker:** 0.9.0_WK_IRPT_FNTEND~30 | **Cell:** FE-s-80 | **Rows fixed:** C-S147, C-S166, W27-S2, W27-S3
| **Portal commit:** `1b6687e1` (LOCAL on `wk-irpt_fntend-13-80-fe-s-80-portal`, portal frozen -- not pushed)

## FIXTURE-FED DISCLOSURE (first, as every prior round)

Every capture below used a real fixture file served over the network-interception plane
(`--fixtures`), never a hand-authored DOM: `src/pages/InvestorReporting/fixtures/smoke/default.json`
(round-12-repaired, 12 concrete entries) for the classifier's end-to-end proof (F80-AC3), and
`__tests__/fe-s-63/fixtures/export-ready.json` for the colour and scroll evidence (Fix 2, F80-AC4),
both reached by a real `--click Export`/`--click Holdings` step, not a hand-built prop. Every run
printed `FIXTURES-MATCH: matched N of N` and (where applicable) `KEY-VALIDITY: k of N valid
consumed.ts operation keys`; verbatim lines are quoted per-criterion below. The dev server ran on
`http://localhost:5960` (this round's own block, 5960-5964; outside the derived range 5400-5899 and
round 12's manual range 5900-5959), stopped and its port confirmed closed (`curl` returned `000`)
before F80-AC5's whole-suite run.

## THE THREE FIXES

**Fix 1 -- the key classifier (C-S166/C-S147), `scripts/ui-smoke.mjs`.** `routeKeyCandidates` used
to return ONE set (`candidates`), truncating every route at its first `{` and requiring
`candidates.has(k)` -- an exact-set test that is right for a static route (no `{param}`: its
candidate IS its whole real path) but wrong for a parameterised one, where a fixture carrying a
concrete value after the prefix (e.g. `/holdings/A-0001` against `GET .../holdings/{accountSetId}`)
is a MORE faithful fixture than the bare prefix and was still rejected. Fixed by splitting into two
DISJOINT sets, populated from disjoint route shapes: `exact` (no-`{param}` routes, full path) and
`prefixes` (the static prefix of a route that HAS a `{param}`). A key is valid when it exactly
matches an `exact` entry OR starts with a `prefixes` entry. Because a static route contributes ONLY
to `exact` and never to `prefixes`, the widening structurally cannot let a static route be satisfied
by prefix-matching -- the round-13 task order's own "No new production defect" bound, verified by a
dedicated BOUND control (below).

**Fix 2 -- the parent-colour command (W27-S2), recorded not coded (graded at L9, AC6).** Round 12's
literal `--expect-style '[data-slot="receipt-panel"]::color=rgb(22, 51, 114)'` reads the receipt-panel
DIV's own computed `color`, which the DIV never sets itself -- it INHERITS navy from `body`'s ambient
`--foreground` (`portal/src/index.css:290`, `portal/design/themes/opal-capital.css:84`,
`--semantic-text-body` = navy `#163372` at `:root`), so it reads the same PASS regardless of what its
descendants render. Read `export/ReceiptPanel.tsx` directly (DESIGN.md C3/C5 cited beside each
change): `[data-slot="flow-placeholder"]` is the ACTUAL descendant with its OWN colour class
(`text-[#6B7280]`, changed from `text-slate-700` by round 12's FE-s-77 fix, per C3's "legal on a
panel" secondary-ink allowance) -- the container merely wraps it. Empirically verified (all four runs
below, port 5960, `export-ready.json`, `--click Export`, idle flow-state -- no receipt exists yet at
this point so `flow-placeholder` is what renders):
```
1. positive, real build:
   EXPECT-STYLE[[data-slot="flow-placeholder"]::color]: PASS rgb(107, 114, 128)
2. wrong-colour control (--inject-css '[data-slot="flow-placeholder"] { color: rgb(0, 255, 0) !important; }'):
   EXPECT-STYLE[[data-slot="flow-placeholder"]::color]: FAIL rgb(0, 255, 0)
3. absent-selector control (same assertion, modal never opened -- no --click Export):
   EXPECT-STYLE[[data-slot="flow-placeholder"]::color]: UNMEASURABLE (selector matched nothing)
4. the OLD literal command, run under the SAME wrong-colour injection as (2):
   EXPECT-STYLE[[data-slot="receipt-panel"]::color]: PASS rgb(22, 51, 114)   <- still PASSES, confounded
```
(1)+(2) together are the wrong-colour discrimination the cell text asks for: the corrected selector
genuinely tells the two states apart. (3) is THE CRITERION RULE part (e), absent-selector. (4) is the
control that PROVES the old command cannot discriminate this defect class at all -- it stays green
even while the actual descendant is painted an obviously wrong colour. GROUND (part d of THE
CRITERION RULE) does not apply: this is a foreground-text (`--expect-style`) assertion, not a
background (`--expect-ground`) one, so there is no ground control to build here.

**Fix 3 -- the visibility/scroll command (W27-S3), `__tests__/fe-s-80/scroll-exercise.mjs` (new,
committed).** Round 12's literal `--expect '[data-slot="preview-scroll"]'` only proves the container
is VISIBLE -- `ui-smoke.mjs`'s own `countVisible()` reads `getBoundingClientRect()` on the element
itself, which reports its own box regardless of ancestor `overflow` clipping, so a scrolled-out-of-view
descendant and a visible one look identical to it (confirmed: `ui-smoke.mjs` contains no `scrollLeft`
write anywhere in its 641 lines). Built a REUSABLE driver (adapts `ui-smoke.mjs`'s own
browser/route/auth-stub mechanism and FE-s-77's `scroll-driver.mjs`'s `scrollLeft` pattern, since
`scripts/` beyond `ui-smoke.mjs` itself sits outside this cell's `<paths>` grant, same constraint
FE-s-77 already documented): `node scroll-exercise.mjs <route> <before.png> <after.png> --port <n>
--selector '<css>' [--fixtures f.json] [--click <name>]... [--width <px>]` -- every route, fixture,
click-step, selector and width is a CLI argument (mirroring `ui-smoke.mjs`'s own flag grammar), and
the content check is GEOMETRIC rather than semantic: it reads EVERY descendant of the container,
keeps the one whose own `getBoundingClientRect().right` extends farthest (viewport coordinates, so
comparable across any nesting depth -- a wrapping `<div>` is normally `width:auto` and never itself
reports the overflow its children cause, which is why immediate children alone are not enough), and
compares that element's rect against the CONTAINER's own rect. This needs no knowledge of what the
scrolled content actually is, which is exactly what "works against an arbitrary container...
without modification beyond the selector argument" requires -- FE-s-84 (wave 2) invokes the same
script against the Reporting tab's 390px report body by changing only `--selector` (and whatever
route/fixture/click-steps reach that state).

Proven against the export modal's own preview container (`[data-slot="preview-scroll"]`, 390px width,
`export-ready.json`, `--click Export` -- the exact W27-S3 scenario):
```
CAPACITY: {"scrollWidth":1056,"clientWidth":264,"scrollLeft":0,"containerRight":327}
FAR-EDGE-BEFORE: {"left":63,"right":1119} CLIPPED
SCROLL-EXERCISED: {"before":0,"after":792,"target":792}
FAR-EDGE-AFTER: {"left":-729,"right":327} NOT CLIPPED
ASSERT-CONTENT: 2 of 2 met
```
`scrollLeft` moved `0 -> 792` (`scrollWidth 1056 - clientWidth 264`) -- the same figure
`__tests__/fe-s-77/scroll-driver.mjs` separately demonstrated -- a real DOM displacement, not a
re-measurement of capacity. The far-edge descendant's own right edge was 792px past the container's
right edge before the exercise (`1119` vs `327`) and lands flush with it after (`327` vs `327`,
`clipped=false`) -- content genuinely off-screen before is genuinely on-screen after, MEASURED
geometrically rather than eyeballed from a screenshot. Absent-selector control run separately: a
wrong selector (`[data-slot="does-not-exist"]`) reads `EXPECT[...]: FAIL (0 visible)` /
`ASSERT-CONTENT: 0 of 2 met`, never a false PASS.

## CRITERIA, IN ORDER

**F80-AC1** -- `bun run typecheck`: `$ tsc -b --noEmit`, `rc=0`. PASS-by-output.

**F80-AC2** -- `bun test .../fe-s-80/key-classifier.test.ts`:
```
POSITIVE   [/api/scoped/investor-reporting/holdings/A-0001]     -> {"valid":1,"total":1}
NEGATIVE   [/api/scoped/investor-reporting/nonexistent-operation] -> {"valid":0,"total":1}
WRONG-SHAPE[/api/scoped/investor-reporting/statuses/REQ-1]      -> {"valid":0,"total":1}
BOUND      [/api/scoped/investor-reporting/status/extra-junk]   -> {"valid":0,"total":1}
N of N controls correct: 3 of 3 controls correct
6 pass / 0 fail / 6 expect() calls
```
PASS-by-output, matching `<expect>` `(?<![0-9])0 fail` verbatim. The test extracts the real
`routeKeyCandidates`/`checkKeyValidity` source from `scripts/ui-smoke.mjs` by balanced-brace count
(string- and regex-literal-aware -- a naive scanner desyncs on `path.indexOf('{')`'s literal brace
and on `checkKeyValidity`'s own `/'([^']*)'/g` regex, whose `'` characters are not string
delimiters) rather than importing the file (which would call `process.exit(2)` before either
function is defined, killing the test process), so it exercises the SHIPPED bytes, never a
hand-copied reimplementation.

**F80-AC3** -- end-to-end, `default.json` (round-12-repaired, 12/12 concrete parameterised keys),
`--click Holdings`:
```
FIXTURES-MATCH: matched 3 of 12
KEY-VALIDITY: 12 of 12 valid consumed.ts operation keys
```
PASS-by-output, matching `<expect>` `KEY-VALIDITY: 12 of 12 valid consumed\.ts operation keys`
verbatim. CONTROL, measured directly by this worker: `scripts/ui-smoke.mjs` swapped for its
pre-fix `HEAD~1` bytes (`git show HEAD~1:scripts/ui-smoke.mjs`, dev server restarted, same
invocation re-run, then restored to the committed fix -- `git diff` clean afterward, confirmed) reads
`KEY-VALIDITY: 5 of 12 valid consumed.ts operation keys`, exactly the count the task order's own
cell text cites -- confirming this fix, not an unrelated change, is what moves `5 of 12` to
`12 of 12`.
`FIXTURES-MATCH: matched 3 of 12` is expected and unrelated to this fix: `default.json` fixtures 12
distinct operations, and clicking only the Holdings tab exercises 3 of them (directory/resolve,
performance, holdings) -- `KEY-VALIDITY` grades the fixture's declared KEYS against the contract,
never fulfilment, so this is not a wire-match defect (`ui-smoke.mjs`'s own header comment: "This is
a SEPARATE, additive line answering the second question; FIXTURES-MATCH is untouched").

**F80-AC4** -- `bun test .../fe-s-80/scroll-instrument.test.ts`:
```
PRECONDITION: dev server on http://localhost:5960 -- MET (... byte-identical to this worktree's package.json)
SCROLL-EXERCISED: {"before":0,"after":792,"target":792}
FAR-EDGE-BEFORE: {"left":63,"right":1119} CLIPPED
FAR-EDGE-AFTER: {"left":-729,"right":327} NOT CLIPPED
ASSERT-CONTENT: 2 of 2 met
2 pass / 0 fail / 11 expect() calls
```
PASS-by-output, matching `<expect>` verbatim. Precondition declared per `1.0.0_SA_CTO` ruling C
(`../fe-s-27/_dev-server.ts`'s own `probeDevServer` re-used with an EXPLICIT port `'5960'` --
this round's own fixed block, never the derived-range fallback, so RULING U's worktree-byte-match
verification still runs unconditionally and a foreign server on 5960 would read FOREIGN, never a
false MET).

**F80-AC5** -- whole-suite bar. Dev server (port 5960) stopped and verified closed (`curl` returned
`000`) before this run; `IRPT_FE_DEV_PORT` unset.
```
643 pass
 24 skip
  0 fail
2678 expect() calls
Ran 667 tests across 124 files. [74.87s]
```
PASS-by-output, matching `<expect>` `(?<![0-9])0 fail` verbatim. F80-AC4's own two tests SKIP inside
this run (server stopped, as required) -- declared by name (`SKIPPED: F80-AC4 -- ...`), not a silent
pass; F80-AC4 itself was already run and PASSED above with the server live.

**F80-AC6** -- JUDGMENT, recorded, no verdict. Evidence:
- Classifier widening (Fix 1): the disjoint `exact`/`prefixes` split, the end-to-end `12 of 12` read
  (F80-AC3), the unit-level POSITIVE/NEGATIVE/WRONG-SHAPE/BOUND controls (F80-AC2) -- the BOUND
  control is the direct proof the widening does not also reach static routes.
- Colour discrimination (Fix 2): the four-run sequence above -- positive PASS, wrong-colour-control
  FAIL, absent-selector UNMEASURABLE, and the OLD command's control-blind PASS under the same
  wrong-colour injection, all against the real build (no --inject-css revert-to-old-code needed; the
  control substitutes for a before/after code diff, per the cell text's own instruction).
- Scroll reusability (Fix 3): the driver's CLI is fully parameterised (route/fixtures/clicks/
  selector/width, no export-modal-specific code anywhere in `scroll-exercise.mjs`), the geometric
  far-edge read needs no knowledge of the scrolled content's semantics, and the real `0 -> 792`
  displacement plus CLIPPED-before/NOT-CLIPPED-after read is reproduced identically whether invoked
  directly (manual probe) or through the `bun test` driver (F80-AC4).

## SURPRISE ROWS FILED

None. Every criterion was satisfied as written; no order defect, no missing capability, no path
outside this cell's grant was needed. Rows C-S147, C-S166, W27-S2 and W27-S3 (all pre-existing,
OPEN, owned by `2.0.0_SA_COO~F`) are the rows this cell's work closes -- their disposition is the
issuer's own act at drain, not a new row from this worker.
