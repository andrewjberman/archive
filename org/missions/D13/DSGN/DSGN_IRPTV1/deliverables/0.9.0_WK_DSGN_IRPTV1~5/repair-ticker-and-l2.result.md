# DSGN_IRPTV1.TO-IV-e-1 (repair-ticker-and-l2) -- result

Worker: `0.9.0_WK_DSGN_IRPTV1~5`. Portal branch `wk-DSGN_IRPTV1-5-portal`, commit
`a380bcb5be9432f1d7612c5af3e12c9480e8a64f` (LOCAL). Workspace branch `wk-DSGN_IRPTV1-5`.

## What changed

**(a) `SecurityList.tsx` `tickerFor()`** -- was `display.symbol` (trimmed) else the tail of
`securityId` split on `:`/`-` (a derived identifier fragment, breaching FWD-11 -- row C-S12).
Now one branch: `display.symbol` (trimmed) when present, else exactly `NOT_SUPPLIED`.
`securityId` is never read, split or printed. Nothing else in the file changed (confirmed by
IVE1-AC3's numstat: 2 added / 6 removed, confined to the function and its docstring).

**(b) `DrillTree.tsx` `mdpfResultFromSnapshot()`** -- each category's direct child now carries
its own `members`: every leaf `security` node beneath that child, any depth, via the same
`leafSecurityMembers` helper the category's own top-level `members` fill already uses, applied
one level down (`children[childLabel(child)] = { aum: ..., members: leafSecurityMembers(child.nodeRef) }`).
No sum. The top-level `members` fill (IV-t-3, round 1) is untouched and re-verified in this
order's own test (`iv-e-1.l2-members.test.ts`'s second test re-derives it and prints
`VERDICT: HERO-FED`). Confirmed confined to the function's ruled span by IVE1-AC3 (three hunks,
base lines 147/198/204, all inside the span [140, 226]).

## IVE1-AC1 -- TICKER-HONEST

`bun test .../iv-e-1.ticker-honesty.test.ts` -- PASS (3 pass / 0 fail, 5 `expect()` calls).
Negative arm: 14 of 14 symbol-less security leaves across all 9 fixtures on disk read exactly
`not supplied`, 0 id fragments found by substring check against each node's own `securityId`.
Positive control: on each of the 6 fixtures carrying at least one security leaf, a
test-side-cloned leaf's `display = {label:'X', symbol:'PLNT'}` prints `PLNT` verbatim from
`securityRowsFrom` AND in the rendered `data-slot="security-ticker"` cell.
`VERDICT: TICKER-HONEST`.

At issuance the negative arm read FAIL (`'1'..'4'` printed on `fe-s-7/holdings.smartx-
observed.json`, verified directly before the fix: `sec:opaque-1`.split(/[:-]/) tail `'1'`) --
this criterion detected the defect it was written against.

## IVE1-AC2 -- L2-FED

`bun test .../iv-e-1.l2-members.test.ts` -- PASS (3 pass / 0 fail, 31 `expect()` calls). Over
all 9 fixtures, every direct child of an L0 category that has leaf securities beneath it (4 of
4 across the set: 2 on `holdings.eclipse-assigned.json`, 1 on `holdings.smartx-observed.json`,
1 on `holdingsSnapshot.success.json`) carries a non-empty `children[label].members` list, set-
equal by `member_id` to the test's own independent recursive walk (9 members total), each
`aum` equal to the source node's own `amount`, each `display_name` following
`display.label`-else-`displayName`. The round-1 top-level fill is re-derived in the same file
and unchanged (`VERDICT: HERO-FED`). `VERDICT: L2-FED`.

At issuance this read 0 members on every child (verified directly: `children` type carried no
`members` field before this fix) -- this criterion detected the defect it was written against.

## IVE1-AC3 -- ONE-FUNCTION

`git show <base>:DrillTree.tsx` located `mdpfResultFromSnapshot`'s span at base lines
`[140, 226]`; `git diff -U0 <base> -- DrillTree.tsx` shows three hunks at base lines `147, 198,
204`, all inside the span. `SecurityList.tsx`'s numstat (`2` added, `6` removed) printed
alongside for the record -- its bound belongs to IV-e-2, not this order. `VERDICT: ONE-FUNCTION`.

## IVE1-AC4 -- RECORD, no verdict (judgment, CVO at L9)

- `iv-e-1.security-list.html` (3862 bytes): `renderToStaticMarkup(createElement(SecurityList,
  {snapshot}))` over `fe-s-7/holdings.cottonwood-target-blend.json` with one leaf's `display`
  planted (`label:'X', symbol:'PLNT'`). 2 rows; ticker cells parsed as `['PLNT', 'not supplied']`
  -- the planted leaf and the untouched leaf, exactly as expected.
- `iv-e-1.hero.html` (14157 bytes): `renderToStaticMarkup(createElement(DrillTree, {snapshot}))`
  over the same (unplanted) fixture. Carries both direct-child labels (`Long Term Target`,
  `Ultra-Long Term Target`). Byte-identical in size to round-1's `iv-t-3.hero.html`: this
  fixture's L0 categories have leaf securities as DIRECT children, so `children[label].members`
  is fed (verified programmatically by IVE1-AC2, not by this static markup) but
  `CategoryViewTree`'s own rendered text for THIS fixture's shape does not change -- the fill's
  visible effect is on an interactive hover/"View breakdown" dialog static markup cannot
  capture. Noted for the CVO in the proof instance and filed as row `DSGN_IRPTV1-W5-S1` (below)
  rather than silently asserted as visually demonstrated.

No PNG named by this order's acceptance battery (unlike round-1's AC4s) -- not attempted, not
declared missing by mistake; see `declared_exclusions` in the proof instance.

## Mutant controls (by hand, restored before commit)

1. `SecurityList.tsx` `tickerFor()` reverted to the pre-fix tail-split. Re-ran IVE1-AC1's test:
   2 of 3 failed (`ABSENT-SYMBOL: 14 of 14 rows not supplied, 14 id fragments`, `VERDICT:
   TICKER-HONEST` did not print). Restored from `.scratch/SecurityList.tsx.good`; `git diff`
   against the committed bytes clean afterward.
2. `DrillTree.tsx` `children[label].members` forced to `[]`. Re-ran IVE1-AC2's test: 2 of 3
   failed (`L2 TOTAL: 4 children checked, 0 members...`), while the round-1 top-level
   re-derivation test in the SAME file still passed (`VERDICT: HERO-FED` printed), isolating
   the failure to the new L2 assertion as designed. Restored from
   `.scratch/DrillTree.tsx.good`; `git diff` against the committed bytes clean afterward.

## Surprise row filed

`DSGN_IRPTV1-W5-S1` (OBSERVATION, INERT) -- this cell's `children[label].members` fill closes
row `W3-S1`'s field-mapping gap for the DIRECT-CHILD level only; the structural gap `W3-S1`
also named (a category whose direct child is itself an intermediate node gets one L1 tile with
no further drill beneath it) is unchanged and out of this cell's field mapping, per the worker
face's own text. Not blocking.

Row `C-S12` (the Ticker derivation) is disarmed by this order's VALID proof instance per the
task order's own round-2 framing (`<round>` line: "rows C-S12 (ARMED, disarmed by this order's
VALID instance)"). That disarm is the REMEDIATION file's (CVO-owned, per Rule 22/§2), not
edited by this worker.
