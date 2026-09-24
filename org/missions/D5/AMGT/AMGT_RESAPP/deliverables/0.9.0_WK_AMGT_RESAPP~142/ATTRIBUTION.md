# AMGT-rm-3 -- THE RESIDUE, MEASURED FIRST -- ATTRIBUTION

`0.9.0_WK_AMGT_RESAPP~142`, round 38, portal DEV base `c7b022a1`. Instrument: `portal/scripts/ui-contract-check.mjs
--port 5184 --scope main --trace --out .../trace/`. Six states run, six `trace.<state>.json` written. Raw run:
`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~142/trace/` (six `trace.<state>.json` plus the
unchanged smoke/measure outputs the `--trace` invocation also produces in the same `--out` directory).

No source file was edited to produce this document -- every attribution below is a `Grep` match against the
CURRENT tree (`portal/src`), read-only.

## 1. Band count, re-keyed (bandContainersTopLevel)

All six states, scope=main: **1 of 1** (PASS -- no element to name; the predicate never fails in this tree
state, confirmed live in the trace run's graded table, reproduced below).

| state | bandContainersTopLevel |
|---|---|
| list | 1 |
| thesis | 1 |
| exec | 1 |
| peers | 1 |
| model | 1 |
| posture | 1 |

## 2. Predicate x state -- count, elements, owning file or UNATTRIBUTED

Every dumped element below was ATTRIBUTED (0 UNATTRIBUTED). The UNATTRIBUTED column is carried on every row so a
future round's residue that this trace's class census patterns cannot resolve has somewhere to land -- none of
today's 18 dumped elements needed it.

| state | predicate | badValue | elementsDumped | tag | class (head) | dataAncestor | owning file | UNATTRIBUTED? |
|---|---|---|---|---|---|---|---|---|
| list | weights | 300 | 1 | SPAN | `font-light tracking-[0.05em]` | none | `src/components/PageHeaderVariants.tsx:46` | no |
| list | weights | 600 | 1 | H3 | `text-sm font-semibold text-white uppercase tracking-wide` | none | `src/ui/components/panels/PanelHeader.tsx:75` | no |
| list | radii | 8px | 1 | DIV | `px-[30px] py-4 border-b border-white/10 bg-[hsl(var(--bg-header))] rounded-t-lg ...` | none | `src/ui/components/panels/PanelHeader.tsx:62` | no |
| thesis | weights | 300 | 1 | SPAN | `font-light tracking-[0.05em]` | none | `src/components/PageHeaderVariants.tsx:46` | no |
| thesis | weights | 600 | 1 | H3 | `text-sm font-semibold text-white uppercase tracking-wide` | data-tab-panel=thesis | `src/ui/components/panels/PanelHeader.tsx:75` | no |
| thesis | sizes | 10 | 1 | SPAN | `` (empty -- inherits font-size) | data-tab-panel=thesis | `src/components/DataTimestamp.tsx:38` (font-size contributed by `PanelHeader.tsx:99`'s `className="text-[10px]"` on the wrapping `DataTimestamp`) | no |
| thesis | radii | 8px | 1 | DIV | `px-[30px] py-4 border-b border-white/10 bg-[hsl(var(--bg-header))] rounded-t-lg ...` | data-tab-panel=thesis | `src/ui/components/panels/PanelHeader.tsx:62` | no |
| exec | weights | 300 | 1 | SPAN | `font-light tracking-[0.05em]` | none | `src/components/PageHeaderVariants.tsx:46` | no |
| exec | weights | 600 | 1 | H3 | `text-sm font-semibold text-white uppercase tracking-wide` | none | `src/ui/components/panels/PanelHeader.tsx:75` | no |
| exec | radii | 8px | 1 | DIV | `px-[30px] py-4 border-b border-white/10 bg-[hsl(var(--bg-header))] rounded-t-lg ...` | none | `src/ui/components/panels/PanelHeader.tsx:62` | no |
| peers | weights | 300 | 1 | SPAN | `font-light tracking-[0.05em]` | none | `src/components/PageHeaderVariants.tsx:46` | no |
| model | weights | 300 | 1 | SPAN | `font-light tracking-[0.05em]` | none | `src/components/PageHeaderVariants.tsx:46` | no |
| model | weights | 600 | 1 | H3 | `text-sm font-semibold text-white uppercase tracking-wide` | none | `src/ui/components/panels/PanelHeader.tsx:75` | no |
| model | sizes | 10 | 1 | SPAN | `` (empty -- inherits font-size) | none | `src/components/DataTimestamp.tsx:38` (font-size contributed by `PanelHeader.tsx:99`) | no |
| model | radii | 8px | 1 | DIV | `px-[30px] py-4 border-b border-white/10 bg-[hsl(var(--bg-header))] rounded-t-lg ...` | none | `src/ui/components/panels/PanelHeader.tsx:62` | no |
| posture | weights | 300 | 1 | SPAN | `font-light tracking-[0.05em]` | none | `src/components/PageHeaderVariants.tsx:46` | no |
| posture | weights | 600 | 1 | H3 | `text-sm font-semibold text-white uppercase tracking-wide` | none | `src/ui/components/panels/PanelHeader.tsx:75` | no |
| posture | radii | 8px | 1 | DIV | `px-[30px] py-4 border-b border-white/10 bg-[hsl(var(--bg-header))] rounded-t-lg ...` | none | `src/ui/components/panels/PanelHeader.tsx:62` | no |

`dataAncestor=none` means no ancestor up to `document.body` carries a `data-*` attribute for that element on that
route (list/exec/model/posture render the header strip OUTSIDE any `[data-tab-panel]` wrapper -- only thesis's
Thesis panel body happens to sit inside one; this is a rendering-structure fact this cell records, not a defect
this cell is chartered to fix).

## 3. Denominators (elements dumped vs elements attributed)

| state | elementsDumped | elementsAttributed | UNATTRIBUTED |
|---|---|---|---|
| list | 3 | 3 | 0 |
| thesis | 4 | 4 | 0 |
| exec | 3 | 3 | 0 |
| peers | 1 | 1 | 0 |
| model | 4 | 4 | 0 |
| posture | 3 | 3 | 0 |
| **TOTAL** | **18** | **18** | **0** |

Cross-check against the trace files' own `totalElementsDumped` fields (`trace.<state>.json`,
`predicates.<name>.totalElementsDumped`, summed per state): list 2+1=3, thesis 2+1+1=4, exec 2+1=3, peers 1=1,
model 2+1+1=4, posture 2+1=3 -- identical to the table above, so this attribution pass dropped nothing between
the trace dump and this document.

**GRAIN NOTE on the "summary" comparison (AC1's own requirement):** weights/sizes/radii are CHARACTER counts in
the graded summary (`j.weights['300']=8` is 8 characters of text at that weight, not 8 elements) -- there is no
pre-existing element count in the summary table for these three predicates to assert equality against, so
`elementsDumped` above is a NEW measurement, reported as such (see each `trace.<state>.json`'s
`summaryFailValue` vs `totalElementsDumped` fields; the console run printed this distinction live, e.g.
`TRACE[thesis.weights] summaryFailValue(char-keyed)=[300,600] elementsDumped(...)=2`). shadows/purpleFills/
bandContainersTopLevel DO carry an element count already (`.length` in `ui-measure.mjs`'s `classify()`) --
none of the three failed in this tree state, so no HOLE/MISMATCH assertion fired this round (would have printed
`HOLE`/`MISMATCH` in the run log had one fired; the log carries neither token for this run,
`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~142/trace_run.log`).

## 4. The residue, attributed

Per the issuer notes: rm-2 (parallel branch, not this cell's tree) owns **weight-300** (`PageHeaderVariants.tsx`)
and the **strip radii, 8px** (`PanelHeader.tsx`/PanelFooter). Everything else failing inside `main` in THIS
tree's current state is the residue nobody has attributed until now:

- **weight-600**: `src/ui/components/panels/PanelHeader.tsx:75` -- the panel title `<h3>` (`font-semibold` =
  CSS weight 600), rendered on every state whose tab supplies a `<PanelHeader title="...">` (5 of 6: list,
  thesis, exec, model, posture; peers' panel does not fail this predicate in `main` scope -- its title strip
  is outside `main`'s measured region, see the round's own `stripContainers[main]=0` reading for peers in the
  graded table above).
- **size-10**: `src/components/DataTimestamp.tsx:38` -- the unclassed `<span>{label}</span>` that renders the
  formatted `generated_at` timestamp, inheriting `font-size:10px` from `PanelHeader.tsx:99`'s
  `className="text-[10px]"` on the wrapping `<DataTimestamp>`. Only 2 of 6 states pass a non-null `timestamp`
  prop into `PanelHeader` (`ThesisTab.tsx:282`, `ModelTab.tsx:346`) -- exec/posture/list/peers's `PanelHeader`
  calls carry no `timestamp` prop (`ExecManagementTab`/`PostureTab.tsx:488`/list's `PanelHeader` usage), so
  `DataTimestamp` never mounts there and the size-10 span never appears on those four states.
- **any non-strip 8px**: NONE FOUND. Every 8px radius dumped in `main` scope, on every state that has one,
  traces to the SAME `PanelHeader.tsx:62` strip container rm-2 already owns -- there is no residue radius left
  over once rm-2's strip fix lands. (Confirmed by exhaustion: `radiiDump` in every `trace.<state>.json` carries
  exactly one key, `"8px"`, with exactly one element, and every one of those six elements' `class` string is the
  identical `PanelHeader.tsx:62` literal.)

## 5. WHAT A FIX WOULD TOUCH (round-39 input)

Distinct owning files across every dumped, attributed element (18 of 18):

| file | elements owned | predicates | states |
|---|---|---|---|
| `src/components/PageHeaderVariants.tsx` | 6 | weights (300) | list, thesis, exec, peers, model, posture (all 6) -- **rm-2's, not residue** |
| `src/ui/components/panels/PanelHeader.tsx` | 10 (5 weight-600 H3 + 5 radii-8px container) | weights (600), radii (8px) | list, thesis, exec, model, posture (5 of 6; peers has neither inside `main`) -- **radii-8px is rm-2's; weight-600 is RESIDUE, unattributed until this cell** |
| `src/components/DataTimestamp.tsx` | 2 | sizes (10) | thesis, model (2 of 6) -- **RESIDUE, unattributed until this cell** (font-size contributed by `PanelHeader.tsx:99`, the same component that owns the weight-600 row) |

**3 distinct files, 18 elements, 0 UNATTRIBUTED.** A round-39 fix for the residue touches two files:
`PanelHeader.tsx` (the title `<h3>`'s `font-semibold` class, line 75) and `DataTimestamp.tsx` (the unclassed
`<span>`, line 38, or its `PanelHeader.tsx:99` caller supplying `text-[10px]`) -- `PageHeaderVariants.tsx` is
rm-2's surface, not this cell's residue, carried here only because its element was dumped in the same trace pass.
