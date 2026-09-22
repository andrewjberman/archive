# FE-s-73 -- census reasons: a component-specific need against a named existing candidate, for every NEW entry

**FIXTURE-FED / EVIDENCE-ONLY NOTICE.** Nothing in this cell touches a live route or a rendered
page. Every measurement below is either a static-source read (the corrected `census.ts` reads
`.tsx` files under `portal/src/pages/InvestorReporting/**` and `portal/src/App.tsx` and does no
network I/O at all) or a `bun test` run over two already-generated JSON artifacts
(`deliverables/0.9.0_WK_IRPT_FNTEND~23/component-census.json`, written by this cell's own run, and
`deliverables/0.9.0_WK_IRPT_FNTEND~14/component-census.json`, FE-s-64's round-10 output, read-only).
This is the right evidence for FWD-12's DONE WHEN on THIS cell (a naming/documentation defect in a
build-time census script, not a rendered surface) and carries no counterpart visual half: the
order itself states this at BOUNDS -- "This cell is not a visual cell: the CTO's four-part rule
does not apply, and it carries its own controls (F73-AC6, F73-AC8). It starts a dev server for
nothing: none is needed." No dev server was started for this cell.

## The defect (row W14-S2), confirmed on the ACTUAL FILES

`render/Page.tsx` defines two components. `PageSheet` (line 340) has NO doc comment directly above
its `export function PageSheet(` -- the nearest preceding comment is a `//` section header three
lines up ("The frame"), separated from the interface and the function by other code. `UnnamedReasonCodeFlag`
(line 115) DOES carry its own leading `/** ... */` block directly above its declaration (lines
110-114): "The flag beside a code the contract does not name. Renders nothing for a named code, an
absent code or an empty one. The code itself is never rewritten: the caller prints it verbatim, and
this sits beside it." FE-s-11's (and FE-s-64's, copied unchanged) `extractHeaderComment` ignored
both facts and took the FILE's first `/** */` block -- the frame comment at the top of the file --
for BOTH components, so FE-s-64's round-10 `component-census.json` shows `PageSheet` and
`UnnamedReasonCodeFlag` with byte-identical `reason` text.

The SAME method defect (confirmed by reading each file directly, not inferred) hits three other
multi-component files in this tree:
- `export/ExportButton.tsx`: `ExportButton` (has its own one-line doc comment) and `ExportAnchorSlot`
  (has its own multi-line doc comment) -- BOTH have own comments, but the round-10 script still gave
  them the file's header text.
- `export/ExportModal.tsx`: `ExportModalPanel` and `ExportModal` -- NEITHER has its own leading
  comment (both are preceded by a `//` section header or a closing brace); this pair's shared reason
  in the corrected output is therefore CORRECTLY marked `FILE-LEVEL (shared)`, not a defect.
- `render/values.tsx`: `Metric` (no own comment) and `SourceValue` (has one: "A plain source value
  (AnalysisReport section values carry their own union).").

## The fix

`extractOwnLeadingComment(fileRel, definitionName)` (new) walks backward from
`export function <definitionName>(` and returns the nearest preceding `/** ... */` block ONLY when
nothing but whitespace separates its closing `*/` from the declaration -- i.e. the comment is
genuinely attached to that one function, not merely present somewhere earlier in the file.
`definitionName` is resolved per import edge (`definitionNameFor`): the exported-name hint for a
`.then(m => ({ default: m.NAMED }))` lazy import, `defaultExportName(relPath)` for a bare default
import (covers `src/App.tsx`'s `InvestorReportingPrint` alias, whose real defined name is
`PrintEntry`), otherwise the local binding (which IS the real export name for every ordinary named
import in this tree -- confirmed by a targeted search: no tree-internal component import uses `as`
aliasing today). When no own comment exists, the row falls back to the file's leading block
(`extractHeaderComment`, unchanged from FE-s-11) and is marked `reasonScope: "FILE-LEVEL (shared)"`;
with neither, `reasonScope: "NONE"` and the original generic fallback text.

Confirmed on the corrected run (`component-census.json` in this folder):

| component | reasonScope | reason |
|---|---|---|
| PageSheet | FILE-LEVEL (shared) | "FE-s-4 -- the page frame both templates share: sheet, header, footer." |
| UnnamedReasonCodeFlag | OWN | "The flag beside a code the contract does not name. Renders nothing for a named code, an absent code or an empty one. The code itself is never rewritten: the caller prints it verbatim, and this sits beside it." |
| ExportButton | OWN | "`data-slot=\"export-button-control\"` names this control for the smoke instrument and tests alike." |
| ExportAnchorSlot | OWN | "Finds the named disabled control, hides it, and portals `ExportButton` into its parent. Renders null when the anchor is not (yet) in the DOM -- the inactive tab, or a tab not yet mounted." |
| ExportModalPanel | FILE-LEVEL (shared) | "FE-s-9 -- the export modal: branding, the narrative toggle, account detail, the optional sections." |
| ExportModal | FILE-LEVEL (shared) | (same as ExportModalPanel -- correct, neither has its own comment) |
| Metric | FILE-LEVEL (shared) | "FE-s-4 -- VALUE RENDERING. One place, so the rule is one rule." |
| SourceValue | OWN | "A plain source value (AnalysisReport section values carry their own union)." |

Census output run from `<WS>/portal`: `COMPONENTS: 73 (REUSED 28, NEW 45)` -- the same population
as round 10 (this fix changes REASON TEXT and adds two new fields; it adds and removes no
component, since classification tracks import edges, which are unchanged).

## `needs` / `nearestExisting` -- every NEW entry (F73-AC5)

Every one of the 45 NEW rows now carries a `needs` sentence (what this component does that the
named `nearestExisting` candidate cannot) and a `nearestExisting` field naming that candidate, drawn
from `NEEDS_TABLE` in `census.ts` -- a hand-written, per-component table (never invented at
runtime), cross-checked against this tree's actual 28-row REUSED set and its own sibling
components. `NEEDS-MISSING: 0` on the corrected run: the table covers all 45 rows FE-s-64's round-10
census enumerated, so no row is left with an invented reason. See `component-census.md` in this
folder for the full table (`needs (nearest existing)` column).

Three rows (`TabShell`, `ClientSearch`, `FirmDropdown`) are named explicitly in their own `needs`
text as THIN WRAPPERS over a REUSED primitive -- see the scope boundary note below.

## Scope boundary, stated once (task point 3)

Carried verbatim into `component-census.json`'s `scopeBoundaryNote` field and into
`component-census.md`'s "Scope boundary" section:

- **SELF-USE**: a component defined and rendered only from within its own defining file (no import
  edge exists to enumerate) is still one census row, keyed `(self -- no import statement; mounted
  from within its own defining file)` -- `ExportButton` and `ExportModalPanel` are this case.
- **WRAPPERS**: `TabShell`, `ClientSearch` and `FirmDropdown` each compose a REUSED primitive (the
  tab-strip component, the `Combobox` family, `PageSurfaceControl`) with little logic of their own
  beyond that composition. They stay classified NEW by the SAME rule this script applies
  everywhere: classification tracks WHERE a component is DEFINED (inside
  `src/pages/InvestorReporting/**`), never how much new logic it adds over what it wraps. Each
  still carries its own `needs`/`nearestExisting` entry naming the primitive it wraps and what the
  wrap adds.

## Controls (F73-AC6, F73-AC8)

The SAME check function (`passesNeedsCheck` in `reasons.test.ts`) is run over both the corrected
census (this order's) and FE-s-64's round-10 census, read-only:

```
REASONS: 45 of 45 NEW entries name a component-specific need and a nearest existing candidate
CONTROL: round-10 census FAILS the same check
REASON-COPY: UnnamedReasonCodeFlag differs from PageSheet
CONTROL: round-10 census had identical reasons for UnnamedReasonCodeFlag and PageSheet
```

The round-10 census never computed `needs`/`nearestExisting` at all, so every one of its 45 NEW
rows fails the check trivially (`0 of 45` pass) -- confirming the check can tell a role label from a
stated need, rather than passing anything handed to it. The reason-copy control reads the round-10
JSON directly and confirms `UnnamedReasonCodeFlag.reason === PageSheet.reason` there (byte-identical
strings), the artifact-level fact row W14-S2 names.

## Tests run

- `bun test src/pages/InvestorReporting/__tests__/fe-s-73/reasons.test.ts` -- 4 pass, 0 fail, run
  TWICE for determinism (both runs printed the identical four control lines above, byte-for-byte).
- `bun test src/pages/InvestorReporting` (whole suite, `IRPT_FE_DEV_PORT` unset, no dev server of
  this worker's running) -- 616 pass, 22 skip, 0 fail, 638 tests across 115 files (one more file
  than round 10's 114, this cell's own `reasons.test.ts`).
- `bun run typecheck` -- `tsc -b --noEmit`, rc=0.

## Surprises

None filed. `NEEDS-MISSING: 0` -- no NEW component was left without a stated need, so the "a
component whose need you cannot state is a finding" clause did not fire. No defect requiring a
write outside this cell's grant (`__tests__/fe-s-73/` and this deliverables folder) was found.

## F73-AC10 (judgment, RECORD only, no verdict)

Every one of the 45 NEW entries in `component-census.json` carries a `needs` field naming what it
does that its `nearestExisting` candidate cannot, and a `nearestExisting` field naming that
candidate by name (drawn from the 28-row REUSED set or another component already defined in this
tree). The scope boundary (self-use rows, and the three thin-wrapper rows) is stated once, in
`scopeBoundaryNote`, carried into both output files. `UnnamedReasonCodeFlag`'s `reason` is now its
own JSDoc (`reasonScope: "OWN"`), differing from `PageSheet`'s file-level fallback text -- the
copied-reason defect row W14-S2 named is fixed on this copy. Three pairs of multi-component files
were checked by hand against their actual source (`ExportButton.tsx`, `ExportModal.tsx`,
`values.tsx`); one pair (`ExportModalPanel`/`ExportModal`) legitimately shares a `FILE-LEVEL
(shared)` reason because NEITHER has its own leading comment -- that is not a re-occurrence of the
defect, it is the disclosed fallback working as designed. No entry's `needs` text was invented: each
cites either the component's own leading JSDoc, its usage context (from FE-s-64's recorded
`usedIn` list), or a named PRD reuse-row precedent already on record in `component-census.md`'s PRD
PATHS table. A reviewer who disputes any one `nearestExisting` candidate can do so directly against
the named component, since every candidate named is a real row in this same census (REUSED or NEW).
