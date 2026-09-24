# DSGN_IRPTV1.TO-IV-t-1 -- result file (`0.9.0_WK_DSGN_IRPTV1~1`)

## IV1-AC1 -- built behaviour (bun test)

PASS by output. `VERDICT: IDENTITY-CARD-OK` (1 pass / 0 fail, 9 `expect()` calls).
WHO: entry displayName present=true; firm displayName present=true.
CHIPS: 2 of 2 (both clean -- name + masked tail, no id leaked).
HOW MUCH: with snapshot -> `$6,024,455.54` present; without snapshot -> `value pending` present, no zero leaked.
AS OF WHEN: `2026-09-09` present.
Full invocation output captured verbatim in the WORKER REPORT.

## IV1-AC2 -- indicator + vocabulary difference control (bun test)

PASS by output. `VERDICT: INDICATOR-AND-VOCAB-OK`.
`ARM1: present ARM2: absent ARM3: clean CONTROL: found`.

## IV1-AC3 -- the ruled touch (CTO 100467, AMENDED mid-order; supersedes 100332)

PASS by output. `NUMSTAT: ['2\t2\tsrc/pages/InvestorReporting/index.tsx']` /
`CHANGED-LINES: 4 OUTSIDE-MOUNT-OR-IMPORT: []` / `VERDICT: MOUNT-PLUS-IMPORT`.

**History, stated plainly (not a criterion, an implementation note):** this criterion originally
read CTO 100332's exact `1 1` numstat bound. A faithful, non-aliased rename of the mount (changing
BOTH the import statement at `index.tsx:19` AND the JSX identifier at `index.tsx:186`) is a genuine
2-line diff -- git numstat sums insertions/deletions across the WHOLE file, not per hunk, so
touching two distinct lines always totals `2 2`, never `1 1`. This worker's first commit
(`3427e8a7`) hit the `1 1` bound via an aliased import (`import { IdentityCard as ScopeSummary }
from './header/IdentityCard'`, JSX text left reading `<ScopeSummary .../>` though the rendered
component was genuinely `IdentityCard`) and filed row `DSGN_IRPTV1-W1-S2`. Mid-order, the issuer
(`2.0.0_SA_COO~D`) relayed CTO ruling 100467 (batch 34), re-bounding the criterion to "the ONE
mount line PLUS at most ONE import line, nothing else" -- explicitly because the original bound
"could not be met by any new component". This worker's second commit (`fe189e4c`) reverted the
alias for the faithful rename the cell always described: `index.tsx:19` now imports `IdentityCard`
directly (the now-unused `ScopeSummary` import removed), `index.tsx:186` reads `<IdentityCard
scope={selectedScope} selection={acceptedNarrowing} row={accepted ? row : null} />`.
`header/ScopeSummary.tsx` is untouched throughout both commits. Confirmed by
`./node_modules/.bin/tsc --noEmit -p tsconfig.json` rc=0, 0 diagnostics, and by IV1-AC1/AC2
exercising the real `IdentityCard` module directly (unaffected by the mount change). Recorded as
rows `DSGN_IRPTV1-W1-S2` (original tension, superseded) and `DSGN_IRPTV1-W1-S4` (the amendment and
the revert) in the investigation file.

## IV1-AC4 -- judgment (CVO at L9), RECORD only, NO VERDICT

Static markup: `iv-t-1.identity-card.html` (this folder), rendered via `renderToStaticMarkup` over
the real `IdentityCard` component with `resolvedScope.success.json` / `directoryEntry.success.json`
/ `holdingsSnapshot.success.json` (adapted: `accountEntries` built from `directoryEntry.success.json`'s
own shape, one clone per `permittedAccountIds` entry, per the cell's "Fixtures (adapted shape)"
clause).

`node scripts/ui-smoke.mjs investor-reporting <dir>/iv-t-1.png --port 5178 --fixtures
src/pages/InvestorReporting/fixtures/smoke/fe-s-14-cottonwood.json` DID run (rc 0, PNG saved,
1440x900, canvas `rgb(244, 246, 250)` = DESIGN.md C3 page field). Its own printed diagnostics:
`FIXTURES-MATCH: matched 1 of 2` and `FIXTURE-DEAD (declared, NEVER matched): /api/scoped/
investor-reporting/performance/` -- the fixture set did not drive `resolve-scope` to a resolved
state in this run, so the live page shows "Scope could not be resolved. Nothing below is scoped,
so nothing below is shown." and `IdentityCard` never mounts in this particular PNG (the branch at
`index.tsx` that renders it is the `selectedScope` truthy branch, which this fixture run did not
reach). This is recorded, not repaired -- a smoke-fixture wiring gap outside this cell's `<paths>`
(fixture routing / `resolve-scope` mock plumbing), not an `IdentityCard` defect: IV1-AC1/AC2 exercise
the component directly and both PASS. The static markup HTML is therefore the reliable render for
`3.0.0_SA_CVO`'s DESIGN.md C1/C2/C3/C8/C9 read; the PNG is included for completeness with this
caveat stated.

Component law self-check against `portal/DESIGN.md` (my own read, not a verdict): `Panel
variant="nested"` (white surface `#FFFFFF`, hairline border, no shadow) + `PanelHeader` +
`PanelContent` per the cell's component law; every ink value is `hsl(var(--palette-navy))` /
`hsl(var(--palette-darkGray))` -- no `text-slate-*` idiom; `tabular-nums` on the custody total and
the business date (C2); no filled/primary action anywhere in the card (C8); weights used are only
`font-normal` (400) and `font-bold` (700) (C1).
