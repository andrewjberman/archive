# DSGN_IRPTV1.TO-IV-t-2 -- performance headline -- result

Worker: `0.9.0_WK_DSGN_IRPTV1~2`. Workspace worktree `wk-DSGN_IRPTV1-2` on workspace base
`e4552e6a053ed6addc20f50994f60a4e33e4748d`; portal worktree `wk-DSGN_IRPTV1-2-portal` on portal base
`7c542fd23ec70c88bade4e3270f4c87f267a275a`.

## What was built

- `portal/src/pages/InvestorReporting/tabs/reporting/PerformanceHeadline.tsx` -- new `Panel
  variant="nested"` component: four tiles (period return via the reused
  `periodReturnForAnsweredWindow` selector from `render/performance/Summary.tsx`; vs-benchmark
  spread read defensively off `benchmarks[0].spread` with no computation; ending/beginning value
  read directly off `report.endingValue`/`report.beginningValue`/`report.valuationCurrency`), a
  `PanelFooter` line carrying `availability.state` plus a `HelperTip` popover carrying state,
  `availability.publicReasonCode`, `sourceTimestamps.businessAsOf` and `revision.revisionId`. The
  word for an absent/unsupported value is exactly `"not supplied"`, never `UNAVAILABLE`, never a
  zero, never an `unavailableReason` code -- `render/values.tsx`'s `Metric` is intentionally NOT
  reused because it prints both of those.
- `portal/src/pages/InvestorReporting/tabs/reporting/ReportingTab.tsx` -- mounted
  `PerformanceHeadline` in place of `Summary` at the named line; the now-dead `Summary` import was
  removed and a `PerformanceHeadline` import added (see IV2-AC3 below -- this makes the diff wider
  than the ruled one line).
- `portal/src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-t-2.headline.test.ts` and
  `iv-t-2.spread-branches.test.ts` -- the two acceptance test files IV2-AC1/AC2 invoke.
- `iv-t-2.headline.html` (this folder) -- static markup of `PerformanceHeadline` over
  `performanceReport.success.json`, via `renderToStaticMarkup`.
- No PNG: no vite dev server was running in this session (`localhost:5175`/`5173` both refused
  the connection) and standing one up was outside this cell's bounds and this order's named
  invocations; IV2-AC4's PNG half is worded "if ... runs for you", so its absence is recorded, not
  repaired. The static markup above is the record IV2-AC4 requires.

## IV2-AC1 -- HEADLINE-OK

```
SUCCESS FIXTURE: fact=YTD supported=true expectedPeriodText='9.17%' textPresent=true labelPresent=true notSuppliedCount=3 (>=2 expected, beginning+ending both absent)
INJECTED SUPPORTED VALUES: beginning present=true ending present=true currency present=true
UNAVAILABLE-METRIC FIXTURE: notSuppliedCount=3 noMetricNotSupported=true noValueNotSupported=true noWindowReasonConstant=true (NO_RETURN_FOR_WINDOW='no-summary-return-for-answered-window')
VERDICT: HEADLINE-OK

 1 pass
 0 fail
 14 expect() calls
```
PASS -- matches `<expect>VERDICT: HEADLINE-OK</expect>`.

## IV2-AC2 -- SPREAD-BRANCHES-OK

```
ARM A: benchmarks carry no spread=true tile='not supplied' computedDifference=1.43% leaksIntoMarkup=false
ARM B: injected spread.value=0.011 expectedText='1.10%' present=true
ARM-A: not supplied ARM-B: 1.10%
VERDICT: SPREAD-BRANCHES-OK

 1 pass
 0 fail
 6 expect() calls
```
PASS -- matches `<expect>VERDICT: SPREAD-BRANCHES-OK</expect>`.

## IV2-AC3 -- superseded FAIL, then PASS on the issuer's amendment

**Attempt 1 (pre-amendment text, CTO ruling 100332 -- REFUSED, measured MOUNT-WIDER-THAN-RULED):**

```
NUMSTAT: ['2\t2\tsrc/pages/InvestorReporting/tabs/reporting/ReportingTab.tsx']
VERDICT: MOUNT-WIDER-THAN-RULED
```

The order's original text ruled the touch to exactly one added and one removed line. Mounting a
NEW component that must be imported cannot be a 1-line diff (the render-line swap is one change;
the import is a second). Removing the now-dead `Summary` import (rather than leaving it unused)
made the true diff 2 added / 2 removed, wider than even the order's own worked example (2/1) --
but still not the ruled 1/1, so the criterion was REFUSED with the measured numstat, per the
order's own instruction: "do not widen silently." Reported, not repaired, in commit
`c480eed9653e12bfc81a72ca5974d55ad829baaf` on this branch.

**Attempt 2 (post-amendment text, issuer `2.0.0_SA_COO~D` on CTO ruling 100467 batch 34, landed at
workspace commit `09bec77ee3e56956170d0bbce99663a799cb08a7` -- PASS):**

The issuer re-bounded IV2-AC3 to "the ONE mount line PLUS at most ONE import line, nothing else"
(numstat 2/1 or 2/2, every changed line an import statement or the mount), confirming attempt 1's
refusal was correct and superseding the 1/1 bound it was measured against. The same portal bytes
already committed at `03979434f4a6f62fd71e56479779fa0e795bf83e` were re-measured against the
amended invocation, unchanged -- no portal edit was needed or made:

```
NUMSTAT: ['2\t2\tsrc/pages/InvestorReporting/tabs/reporting/ReportingTab.tsx']
CHANGED-LINES: 4 OUTSIDE-MOUNT-OR-IMPORT: []
VERDICT: MOUNT-PLUS-IMPORT
```
PASS -- matches `<expect>VERDICT: MOUNT-PLUS-IMPORT</expect>`. All 4 changed lines are either an
`import` statement (the `Summary` import removed, the `PerformanceHeadline` import added) or the
mount swap itself (the `Summary report=` line out, the `PerformanceHeadline` line in) -- 0 lines
outside that set.

## IV2-AC4 -- RECORDED, no verdict (judgment; graded by `3.0.0_SA_CVO` at L9)

Static markup: `iv-t-2.headline.html` in this folder (rendered over
`performanceReport.success.json`). No PNG produced -- see "What was built" above.

## Surprises

None filed on this cell -- every fact needed (the `spread` shape, the optional
beginning/ending/currency fields, the exact mount line and its base bytes) was already named or
directly readable in the order and the base repo; the only deviation from the order's literal text
(IV2-AC3's diff shape) is a REFUSAL the order itself pre-authorizes and names the exact form of
("do not widen silently"), not an off-mandate discovery, so it is reported as a refused criterion
above rather than filed as a surprise row.
