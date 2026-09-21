# IRPT_FNTEND.TO-FE-s-60 -- result log (0.9.0_WK_IRPT_FNTEND~10)

## What was built

`portal/src/pages/InvestorReporting/render/narrative/PeriodInContextPage.tsx` gains ONE new
conditional JSX node, sited immediately after the `fixed-statement` paragraph and before the
chart, reading `packet.availability.unprojectedGrant` directly (no re-derivation of
count/denominator/kinds; `NarrativePacket extends ContractEnvelope`, so `.availability` is
already reachable on the prop as typed):

```tsx
{packet.availability.unprojectedGrant && packet.availability.unprojectedGrant.count > 0 ? (
  <p
    className="ir-note ir-muted"
    data-block="partial-disclosure"
    data-slot="partial-disclosure"
    data-count={packet.availability.unprojectedGrant.count}
    data-denominator={packet.availability.unprojectedGrant.denominator}
  >
    {packet.availability.unprojectedGrant.count} of {packet.availability.unprojectedGrant.denominator}{' '}
    {packet.availability.unprojectedGrant.kinds.join(', ')} not yet reflected in this narrative.
  </p>
) : null}
```

`compose.ts` was NOT touched -- the field is reachable directly off the `packet` prop, so no
surfacing through the composition was needed (per BOUNDS, confirmed before touching the file).

Reuses the file's own `ir-note ir-muted` idiom verbatim (the `narrative-coverage` paragraph,
`:188-190`, is the precedent named by the cell text), and pairs `data-block`/`data-slot` with
the SAME value `"partial-disclosure"`, matching the file's own root-section convention
(`data-block="period-in-context-page"` / `data-slot="fe-s-8"`, `:94`).

**One render, both consumers, confirmed rather than assumed:** `render/performance/
PerformanceDocument.tsx:128` mounts `PeriodInContextPage` with `{packet, report}` for the
print/PDF path -- the identical component this cell edited, no second copy exists anywhere in
this commit's diff. F60-AC4's test renders the SAME packet object once standalone and once via
`PerformanceDocument`, and confirms the two markups' `partial-disclosure` node strings are
byte-identical (see the test's `PREVIEW NODE` / `PDF NODE` lines).

New test file: `portal/src/pages/InvestorReporting/__tests__/fe-s-60/period-in-context-badge.test.ts`.

## Criteria, measured at portal HEAD `0de19364` (workspace worktree branch
`wk-irpt_fntend-9-60-fe-s-60`)

- **F60-AC1** (whole portal typecheck): `rc=0`.
- **F60-AC2** (renders when count>0, names count/denominator/kinds verbatim): PASS, node text
  `1 of 5 events not yet reflected in this narrative.`
- **F60-AC3** (absent when count=0 and when null, both arms): PASS, both arms print `ABSENT`.
- **F60-AC4** (one render, both consumers): PASS, `PREVIEW NODE` and `PDF NODE` are the
  identical string.
- **F60-AC5** (whole IRPT_FNTEND suite green): `606 pass, 21 skip, 0 fail, Ran 627 tests across
  112 files.`
- **F60-AC6** (judgment -- color law + genuine shared render): RECORDED, no verdict. See below.

## Mutant + determinism controls

**Mutant:** temporarily replaced the guard `packet.availability.unprojectedGrant &&
packet.availability.unprojectedGrant.count > 0` with an unconditional `true`, re-ran the new
test file. Result: F60-AC3's test FAILED -- the `count:0` arm now rendered the node (should be
absent), and the `null` arm threw `TypeError: null is not an object (evaluating
'packet.availability.unprojectedGrant.count')` inside `renderToStaticMarkup`. Reverted
immediately; `git diff --stat` on the source file after revert is empty (byte-identical to the
committed version) and the full test file passes again (3 pass, 0 fail).

**Determinism:** ran `bun test .../fe-s-60/period-in-context-badge.test.ts` twice at the same
committed HEAD; both runs print identical `NODE:`, `PREVIEW NODE:`, `PDF NODE:` lines and
`3 pass, 0 fail`.

## F60-AC6 record (judgment -- no verdict taken by this worker)

**Color law citation drift (filed as surprise `IRPT_FNTEND-W10-S1`):** the cell text says to
confirm the idiom "by reading `src/index.css`'s `.ir-note` rule" -- but `src/index.css` (806
lines) carries NO `.ir-note` or `.ir-muted` rule at all (Grep, zero matches). Both classes are
defined in `render/print.css:272-277` / `:285-287`:

```css
.ir-note {
  font-size: 11px;
  line-height: 1.45;
  color: #595959;
  margin: 6px 0;
}
.ir-muted {
  color: #595959;
}
```

`#595959` is a dark grey. Portal `CLAUDE.md`'s color law table (`:36-37`) names page-canvas ink
as navy-only `#163372` and panel secondary ink as `#6B7280` -- neither row names `#595959`.
This is `render/print.css`'s own PRE-EXISTING print/export-document convention (used
throughout this same file already, e.g. `narrative-coverage` and `missing-history`/
`missing-history-reason`, none newly introduced by this cell): this cell's new node reuses
that existing idiom VERBATIM and introduces no new color of its own. Whether a printed-
document stylesheet is in scope for the interactive-canvas color law (the table is headed
"page canvas" / "panel" / "band") is left for L9 to rule on.

**No screenshot capability (filed as surprise `IRPT_FNTEND-W10-S2`):** BOUNDS instructs
"render and read a screenshot before reporting F60-AC6." This worker's tool set (Bash, Read,
Write, Edit, Glob, Grep) carries no browser-automation or screenshot tool, and the portal
package has neither `playwright` nor `puppeteer` as a dependency (grepped, 0 matches) -- no
in-repo mechanism produces one either. F60-AC6 is therefore recorded from (1) the
`renderToStaticMarkup` output already printed by F60-AC2/AC3/AC4's test (real DOM text, not
assumed) and (2) the direct CSS-source citation above, never a rendered screenshot. A sibling
deliverable on this same project (worker `~4`, FE-s-7, F7-AC7) DID attach two PNG screenshots
to its own judgment record, so screenshot capability existed for at least one prior worker
session on this project; this session does not have it.

**Whether F60-AC4 genuinely proves one shared render path:** yes, by construction and by
measurement together -- the source diff (`git show 0de19364 --name-only`) touches exactly one
`.tsx` file (`PeriodInContextPage.tsx`) and adds exactly one JSX node; `PerformanceDocument.tsx`
is unmodified in this commit and its own `PeriodInContextPage` mount (`:128`) is the
pre-existing FE-s-8 wiring. The test does not merely compare two renders that "happen to look
the same" -- it constructs ONE packet object and passes the SAME object into both call sites,
so an identical string is the necessary consequence of one shared component reading one shared
prop, not a coincidence between two independently-written copies.
