# IRPT_FNTEND.TO-FE-s-67 -- result (0.9.0_WK_IRPT_FNTEND~17)

**FIXTURE-FED, NOT LIVE.** Every capture below answers a route with fixtures served AT THE
NETWORK LAYER (`--fixtures`, `scripts/ui-smoke.mjs`, or the equivalent scenario-map input to
`__tests__/fe-s-32/holdings-driver.mjs`); no live backend route was reached. That is the right
evidence for THIS card: FWD-12's DONE WHEN ("the Investor Reporting screens look and behave like
the rest of the Opal portal") is a claim about RENDERING and BEHAVIOR under a known, named state --
whether a red-text block is now `PanelError`, whether a button is `buttonClass('secondary', ...)`,
whether a breadcrumb carries an at-rest underline -- and every one of those is fully determined by
the fixture the browser is handed, not by whether the network route is live. It is NOT the right
evidence for the other seven PRD cards this project carries (live data correctness, real latency,
real auth, etc.), which is why this card is graded on fixture-fed captures and no wire-integration
claim is made anywhere in this file.

## Base and mechanics

- Workspace at the round-11 issuance commit on CLOUD; portal DEV `0054b81d3c277539dd4f370e02cb8066cd2543a1`
  plus this cell's own commit `3f69c95c09bf6a937daf67c94af931f29676d810` (portal repo, local only,
  PORTAL IS FROZEN).
- Dev server: `IRPT_FE_DEV_PORT=5920 bun run dev --port 5920` (port verified free via curl before
  starting, verified closed via curl `000` after every stop). All ten mechanical criteria (F67-AC1..AC10)
  ran with the server up; F67-AC11 (the whole-suite bar) ran AFTER the server was stopped and its port
  confirmed closed (PowerShell `Get-NetTCPConnection -LocalPort 5920 -State Listen` + `Stop-Process`),
  in a shell with `IRPT_FE_DEV_PORT` unset (`env -u IRPT_FE_DEV_PORT`).
- Read DESIGN.md C1-C12 and portal/CLAUDE.md in full before starting; PRD FWD-12's ENDPOINT row and
  the CTO's round-10 analysis (both named in the order) read at HEAD.

## Fixes made (BEFORE/AFTER, one per finding, cited to clause)

1. **`index.tsx:104-110` (C12 -- never a red block of text on the bare canvas).** BEFORE:
   `<p className="text-sm text-red-800">Scope could not be resolved...</p>`. AFTER: wrapped in
   `<PanelError surface="panel" message="Scope could not be resolved. Nothing below is scoped, so
   nothing below is shown." />` inside a `<div data-slot="scope-error">` (PanelError's `Frame` does
   not forward arbitrary props, so the data-slot lives on the wrapper; F67-AC2's selectors target
   PanelError's own descendants -- `svg`, `p` -- so no separate ink class was needed on this wrapper).

2. **`tabs/StatusPanel.tsx:102-113` (C8 -- one persistent primary action per view; C12).** BEFORE:
   the safe-action button was `bg-[hsl(var(--primary))] ... text-white` -- a SECOND filled-primary
   alongside Export. AFTER: `buttonClass('secondary', 'canvas', 'sm')` from `src/ui/components/
   Controls.tsx` (white fill, navy border, navy label). MUTANT CONTROL (see below): reverting this one
   line makes F67-AC4's style assertions FAIL exactly as expected (`rgb(95, 59, 227)` / `rgb(255, 255,
   255)` instead of white / navy), confirming the assertion discriminates and was not a vacuous pass.

3. **`tabs/analysis/GenerateComposer.tsx`, three blocks (C12).** `composer-refusal` (:356-361 pre-fix),
   `comparison-refusal` (:289-293 pre-fix) and `snapshot-remainder` (:237-242 pre-fix) were each a bare
   `<p className="text-xs text-red-800" ...>` / `<p className="text-sm text-red-800" ...>`. AFTER: each
   wrapped in `<PanelError compact .../>` (composer-refusal non-compact, matching its original text-sm),
   `surface="inset"` (default -- an inline form refusal, no host panel, no retry). FINDING mid-fix: the
   FIRST pass (wrapper carrying only `data-slot`, no ink class) PASSED content assertions but FAILED
   F67-AC5's style assertion on `snapshot-remainder` (`EXPECT-STYLE[...color]: FAIL oklch(0.372 0.044
   257.287)` -- the wrapper was INHERITING its ancestor's `text-slate-700`, because `composer-snapshot`'s
   own container sets that colour and PanelError's `Frame` (the element that actually carries the navy
   ink class) is a CHILD of the wrapper, not the wrapper itself, so colour does not cascade upward. Fixed
   by adding PanelError's own ink class (`text-[hsl(var(--palette-navy))]`, the literal token PanelStates.tsx
   uses internally) to all three wrappers explicitly; re-ran, `ASSERT-STYLE: 2 of 2 met`. A control is a
   claim: this is exactly that lesson, caught before reporting a false PASS.

4. **`tabs/holdings/DrillTree.tsx:178-186` (C8 -- the five identity accents are named and a tree
   breadcrumb is not one of them, DESIGN.md :354-357).** BEFORE: `hover:underline` only (no at-rest
   underline). AFTER: `underline` (at-rest), colour KEPT (`text-[hsl(var(--primary))]`, unchanged) --
   the colour question is a genuine judgment call the order does not make, recorded for the CVO at
   F67-AC12 and NOT self-graded.

5. **`tabs/holdings/DrillTree.tsx:234` (C12).** BEFORE: bare `<p className="text-xs text-red-800">`.
   AFTER: wrapped in `PanelError compact` (same ink-class fix as #3, same reason), `surface="inset"`
   (already inside the white `holdings-drill-tree` panel), no retry. NOT CONFIRMED REACHABLE -- see
   row `IRPT_FNTEND-W17-S1`: measured (not merely un-fixtured) STRUCTURALLY UNREACHABLE, because
   `contracts/adapt.ts`'s `adaptHoldingsSnapshot` derives BOTH sides of the `revisionMismatch` comparison
   (`node.provenance.sourceRevision`, `snapshot.sourceSetRevision`) from the SAME local variable
   (`sourceSetRevision`, adapt.ts:938,965,977). Tried: `fe-s-18-holdings-observed.json`,
   `fe-s-14-global.json` -- neither carries per-node revision data (consistent with the finding). Wrapped
   from source per BOUNDS regardless; named as open at F67-AC12.

## Criteria

**F67-AC1 -- the whole portal typechecks.**
`cd <WS>/portal && timeout 180 bun run typecheck; echo rc=$?` -> `rc=0`. PASS.

**F67-AC2 -- the scope-failure state.** `--fail investor-reporting/directory/resolve`, expects
`[data-slot="scope-error"]` with the failure text, danger icon, navy text.
```
EXPECT[[data-slot="scope-error"]]: PASS (1 visible)
EXPECT-TEXT[[data-slot="scope-error"]::Scope could not be resolved]: PASS
EXPECT-STYLE[[data-slot="scope-error"] svg::color]: PASS rgb(190, 45, 54)
EXPECT-STYLE[[data-slot="scope-error"] p::color]: PASS rgb(22, 51, 114)
ASSERT-CONTENT: 2 of 2 met
ASSERT-STYLE: 2 of 2 met
```
PASS (matches `ASSERT-CONTENT: 2 of 2 met[\s\S]*ASSERT-STYLE: 2 of 2 met`).

**F67-AC3 -- THE CONTENT CONTROL (no `--fail`).** Expected `ASSERT-CONTENT: 0 of 2 met`.

FIRST pass (fixture `default.json`, as originally written): `ASSERT-CONTENT: 2 of 2 met` --
**FAIL, measured, REFUSED as written.** Root cause (row `IRPT_FNTEND-W17-S3`, GROUNDED, positive-control
confirmed): `fixtures/smoke/default.json` omits `unprojected_grant` on ALL 12 of its declared route
entries; `contracts/envelope.ts:278-280` throws `EnvelopeMismatch` on ANY response missing that field,
unconditionally -- so `resolve-scope` genuinely fails under this fixture with or without `--fail`, and
the "control" scenario ("scope resolves normally") is never actually constructed. Patched a SCRATCH copy
of `default.json` (not committed, outside grant) adding the field to `directory/resolve` only, re-ran the
identical invocation against the patch: `ASSERT-CONTENT: 0 of 2 met` -- confirms the fixture, not this
cell's markup, is the cause. `fixtures/smoke/default.json` is outside `<paths>`; not edited. Reported per
BOUNDS, not weakened, not self-graded past the failure.

**AMENDED (COO commit `5cad85da0b`, verified by this worker: `git cat-file -t` resolves, `git show
--name-only` touches ONLY the TO file, both AMENDMENT blocks read directly).** The fixture is swapped to
`fixtures/smoke/fe-s-18-frozen.json` (independently re-verified clean by this worker: 0 of 9 entries
missing `unprojected_grant`). Re-ran the corrected invocation against the same dev server:
```
EXPECT[[data-slot="scope-error"]]: FAIL (0 visible)
EXPECT-TEXT[[data-slot="scope-error"]::Scope could not be resolved]: FAIL
ASSERT-CONTENT: 0 of 2 met
```
**PASS**, matching `<expect>ASSERT-CONTENT: 0 of 2 met</expect>` exactly. Row `IRPT_FNTEND-W17-S3` stays
filed as the record of the original defect; this amendment is its remedy.

**F67-AC4 -- the StatusPanel safe-action button.** `fe-s-14-global.json` (its performance-report response
carries no `status` wrapper, so `EXPLICIT_UNKNOWN_STATE` = `UNCERTAIN` -> not answer-bearing ->
`StatusPanel` renders with `defaultSafeActions('UNCERTAIN', ...)` = `Reload`).
```
EXPECT[[data-slot="safe-actions"] button]: PASS (1 visible)
EXPECT-TEXT[[data-slot="safe-actions"] button::Reload]: PASS
EXPECT-STYLE[[data-slot="safe-actions"] button::background-color]: PASS rgb(255, 255, 255)
EXPECT-STYLE[[data-slot="safe-actions"] button::color]: PASS rgb(22, 51, 114)
ASSERT-CONTENT: 2 of 2 met
ASSERT-STYLE: 2 of 2 met
```
PASS. Content control the order left open (found and authored, not invented -- an EXISTING fixture):
`fixtures/smoke/reporting-answer-bearing.json` (a genuine READY performance-report with `actions: []`)
against the SAME two `--expect` lines: `ASSERT-CONTENT: 0 of 2 met` (the safe-actions slot is not found --
either because `StatusPanel` never mounts for an answer-bearing READY report, or because it mounts with
zero actions; either way the assertion does not vacuously pass). MUTANT CONTROL: reverted StatusPanel's
button class to the OLD `bg-primary/text-white` classes and re-ran F67-AC4's exact invocation ->
`EXPECT-STYLE[...background-color]: FAIL rgb(95, 59, 227)`, `EXPECT-STYLE[...color]: FAIL rgb(255, 255,
255)`, `ASSERT-STYLE: 0 of 2 met` -- fired as expected. Restored via `git checkout --` (file was already
committed at `3f69c95c`); re-ran, `ASSERT-STYLE: 2 of 2 met` again.

**F67-AC5 -- Analysis composer refusal + remainder, navy.**
```
CLICKED: Analysis
EXPECT[[data-slot="composer-refusal"]]: PASS (1 visible)
EXPECT[[data-slot="snapshot-remainder"]]: PASS (1 visible)
EXPECT-TEXT[[data-slot="composer-refusal"]::Select a client in the header first]: PASS
EXPECT-TEXT[[data-slot="snapshot-remainder"]::Needs correction]: PASS
EXPECT-STYLE[[data-slot="composer-refusal"]::color]: PASS rgb(22, 51, 114)
EXPECT-STYLE[[data-slot="snapshot-remainder"]::color]: PASS rgb(22, 51, 114)
ASSERT-CONTENT: 4 of 4 met
ASSERT-STYLE: 2 of 2 met
```
PASS (first pass FAILED on `snapshot-remainder`'s style -- see fix #3 above -- fixed, then re-run to this
result).

**F67-AC6 -- THE CONTENT CONTROL (no `--click Analysis`).**
```
EXPECT[[data-slot="composer-refusal"]]: FAIL (0 visible)
EXPECT[[data-slot="snapshot-remainder"]]: FAIL (0 visible)
ASSERT-CONTENT: 0 of 2 met
```
PASS.

**F67-AC7 -- Holdings breadcrumb + slice table, breadcrumb underlined at rest.**
```
CLICKED: Holdings
EXPECT[[data-slot="holdings-breadcrumb"]]: PASS (1 visible)
EXPECT[[data-slot="slice-table"] thead th:last-child]: PASS (1 visible)
EXPECT-STYLE[[data-slot="holdings-breadcrumb"]::text-decoration-line]: PASS underline
ASSERT-CONTENT: 2 of 2 met
ASSERT-STYLE: 1 of 1 met
```
PASS.

**F67-AC8 -- THE CONTENT CONTROL (no `--click Holdings`).**
```
EXPECT[[data-slot="holdings-breadcrumb"]]: FAIL (0 visible)
EXPECT[[data-slot="slice-table"] thead th:last-child]: FAIL (0 visible)
ASSERT-CONTENT: 0 of 2 met
```
PASS.

**F67-AC9 -- BEFORE capture at 390.** `f67_overflow_before.png` saved (`SAVED : .../f67_overflow_before.png`).
Read: the slice table's last column ("Denom") is visibly clipped at the right edge (`5,000,` -- an
incomplete value, cut mid-digit-group), consistent with `min-w-[640px]` inside `overflow-x-auto` at a
390px viewport. PASS.

**F67-AC10 -- OVERFLOW EXERCISED, reusing `__tests__/fe-s-32/holdings-driver.mjs`.**
LITERAL invocation as written (`--port/--width/--fixtures/--out` flags): **rc=1, crash.** The driver's
real CLI is POSITIONAL (`<port> <scenario-map.json> <captureDir>`, `holdings-driver.mjs:37-39`) and its
input file shape is `{"<scenario>": {"<route-key>": <envelope>, ...}, ...}` (a MAP of scenarios), not a
flat ui-smoke.mjs fixture. `--port` is read as the literal PORT value (wrong), `5920` (the next argv) is
read as the MAP PATH and `readFileSync` throws `ENOENT`. Per the order's own permission ("If this driver's
CLI shape differs from this invocation, adapt the call and say so in your result"), ADAPTED: wrapped
`fe-s-18-holdings-observed.json`'s flat map as one scenario (`{"fe-s-18-holdings-observed": <the same
map>}`) and ran `node .../holdings-driver.mjs 5920 <scenario-map>.json <captureDir>` -> **rc=0, `DRIVER
OK`**. Output (`org/.../deliverables/0.9.0_WK_IRPT_FNTEND~17/f67_overflow/`): four PNGs (390 and 1440,
each a full-page capture plus a `_table_scrolled` capture, since `scrollWidth 826 > clientWidth 260` at
390) and a manifest. The RESULT json's `visibility` before scroll at 390: `{"basis":true,"supervision":
false,"advisory":false}`; after `SCROLL_TO_CLASSIFICATION`: `{"basis":false,"supervision":true,"advisory":
true}` -- the columns clipped in the BEFORE capture (matching F67-AC9's read) ARE brought into view by
scrolling, confirmed by reading BOTH PNGs (`fe-s-32_holdings_fe_s_18_holdings_observed_390.png` and its
`_table_scrolled` sibling): the second shows Supervision / Advisory / Provenance in full where the first
cut them off. **Substantively, the cell's own question is answered: the overflow is reachable by scroll,
not permanently clipped.** **FAIL against the literal `<expect>SAVED|scrollLeft</expect>`, measured, on
BOTH invocations** -- row `IRPT_FNTEND-W17-S2` (GROUNDED): the driver's ONLY `console.log` call sites
(`holdings-driver.mjs:198-228`) print `CAPTURE`/`RESULT`/`  served(...)`/`PAGE CRASHES:`/`DRIVER OK`; the
literal source cannot emit `SAVED` or `scrollLeft` under any invocation shape. `grep -c 'SAVED\|scrollLeft'`
over the full adapted-run log: 0. Reported per BOUNDS, not weakened, not self-graded past the failure.

**AMENDED (COO commit `5cad85da0b`, verified as above).** `<invocation>` corrected to the real positional
shape and `<expect>` corrected to `DRIVER OK` (the driver's own success sentinel). Re-ran with a fresh
scenario-map file (`f67_overflow_scenarios.json`, this worker's own deliverables folder) and a fresh
capture directory: `rc=0`, last stdout line `DRIVER OK` -- **matches `<expect>DRIVER OK</expect>`
exactly, PASS.** Both PNGs re-read, confirming the same scroll-reachability finding as the original run.

**NEW FINDING, row `IRPT_FNTEND-W17-S5` (filed this tick):** the amendment's corrected `<invocation>` text
is itself not a real executable command -- it carries a bracketed span
(`<scenario-map.json, one entry wrapping fixtures/smoke/fe-s-18-holdings-observed.json>`) that is not a
declared placeholder (the TO declares only `WS`, `PORT`) and does not match
`proof-of-spec-check.py`'s `PLACEHOLDER_TOKEN_RE` (`[A-Z][A-Z0-9_]*`, all-caps only). Under this TO's
declared `<placeholders>` (ENFORCE mode), the checker's invocation-alignment limb therefore requires this
row's recorded `invocation` to match that bracketed text LITERALLY -- which no real, re-runnable command
can do. MEASURED: recording this worker's own actual command (the one that produced the passing `DRIVER
OK` result above) makes `python .tools/proof-of-spec-check.py <instance> ... --governing-order <TO>`
(run from inside this worktree) report exactly ONE violation --
`VIOLATION: invocation-alignment[F67-AC10]: the RECORDED invocation is NOT the criterion's invocation
modulo the placeholder(s) ['PORT', 'WS']` -- and `INVALID (rc=1)`. This worker did NOT write the
unexecutable bracket text as its own `invocation` (that would misrepresent what was actually run), and did
NOT further edit the criterion's `<invocation>`/`<expect>` substance (out of this worker's authority per
BOUNDS -- the task-order file is this worker's grant for the `<status>` flip only, not for rewriting
criteria: "an order defect is reported, and the issuer amends it"). So: **F67-AC10's own substantive bar is
met (PASS-by-output, `DRIVER OK`), but the proof-of-spec-check instance as a WHOLE is `INVALID (rc=1)` on
this one mechanical ground, and `<status>` is NOT flipped to `complete`.**

**SECOND AMENDMENT (COO commit `b570ecf546`, verified by this worker the same way: `git cat-file -t`
resolves, `git show --name-only` touches ONLY the TO file, diff read directly against its parent).**
`<invocation>` corrected again -- this time to point at this worker's own already-authored, already-
committed `f67_overflow_scenarios.json` (using only the declared `WS`/`PORT` placeholders, no prose
bracket). This is now EXACTLY the command already run and recorded above. Applied to this worker's own
worktree copy of the TO (working-tree edit; `diff --strip-trailing-cr` against `git show
b570ecf546:<path>` afterward: 0 lines, content-identical). Re-ran `python .tools/proof-of-spec-check.py
<instance> F67-AC1..AC12 --governing-order <TO>` from inside this worktree:
`invocation-alignment (recorded invocation -> criterion text): 11/11 comparable row(s) match modulo
placeholder expansion; 0 diverge`, `violations=0`, **`VALID (rc=0)`.** No new capture was needed -- this
closed against evidence already produced and already committed. Row `IRPT_FNTEND-W17-S5` is now RESOLVED
(the mechanical defect it named is fixed); the row itself stays filed as the record, per the surprise
channel's append-only, never-edit-an-existing-row discipline.

**F67-AC11 -- whole suite green, pinning tests unchanged.** Dev server stopped and port verified closed
(`curl` -> `000`) BEFORE this run; run in a shell with `IRPT_FE_DEV_PORT` unset.
```
622 pass
22 skip
0 fail
2615 expect() calls
Ran 644 tests across 117 files.
```
`fe-s-21/source-age.test.ts`: 99 pass (subset run), 0 fail -- `NO ERROR AFFORDANCE: 4 of 4`, positive
control (7 hits) and negative control (0 hits) both fired as designed; the source-age slot this file
scans is untouched by this cell. `fe-s-11/colour-law.test.ts`: `SCANNED: 41 files`, 0 violations -- every
button this cell introduced or changed is either PanelError-descended (its own INK class covers it) or
self-backgrounded (`buttonClass`'s explicit `bg-`/`text-` pair on the SAME element), so nothing new was
flagged. `__tests__/fe-s-67/panel-error-reuse.test.ts` (this cell's own guard): `PANEL-ERROR IMPORTS: 3 of
3`, `BUTTONCLASS IMPORTS: 1 of 1`, `TEXT-RED-800 OUTSIDE COMMENTS: 0 of 4 files scanned`. PASS.

**F67-AC12 -- judgment, RECORDED, NO VERDICT.**
- Every fix reuses an EXISTING pattern: `PanelError` (`src/ui/components/states/PanelStates.tsx`, 0
  consumers in `InvestorReporting/` before this cell -- confirmed by reading the file's own header
  ("PanelError ... a status.danger icon beside navy text") and this cell's own pre-fix grep of the four
  touched files, none of which imported it) for every red-only text block (index.tsx, and three in
  GenerateComposer.tsx, one in DrillTree.tsx); `buttonClass('secondary', 'canvas', 'sm')`
  (`src/ui/components/Controls.tsx`) for StatusPanel.tsx's safe-action button. Cited to DESIGN.md C12
  (never a red block of text; the four designed states) and C8 (one persistent primary action per view).
- The breadcrumb's colour choice (kept purple-and-underlined, not moved to navy) is the CTO's open call,
  cited to DESIGN.md :352-361 (C8's five named identity places, which a tree-navigation breadcrumb is not
  one of) -- NOT self-graded here.
- Two items this cell could not fully close, named as OPEN, not silently dropped:
  1. The StatusPanel content-control fixture (F67-AC4's open note) -- FOUND, not authored:
     `fixtures/smoke/reporting-answer-bearing.json`, an existing fixture with a genuine READY state and
     zero safe actions, run and reported above (`ASSERT-CONTENT: 0 of 2 met`).
  2. DrillTree `:234`'s revision-mismatch text -- wrapped from source, measured STRUCTURALLY unreachable
     from any fixture through the current adapter (row `IRPT_FNTEND-W17-S1`), not merely un-fixtured.
- Also disclosed for the CVO, not self-graded: F67-AC3 (row `IRPT_FNTEND-W17-S3`, a `default.json` fixture
  defect unrelated to this cell's markup) and F67-AC10 (row `IRPT_FNTEND-W17-S2`, the reused driver's
  output vocabulary never matches `<expect>SAVED|scrollLeft</expect>` under any invocation) both measured
  FAIL as literally written against the ORIGINAL criteria text; both were subsequently amended by the
  issuer (commits `5cad85da0b`, `b570ecf546`) and both now read PASS -- see the criteria section above
  and rows `IRPT_FNTEND-W17-S3`/`S2`/`S5`.
- The cell text's literal "PanelError is imported by all of them [four files]" -- a judgment call, row
  `IRPT_FNTEND-W17-S4`: StatusPanel.tsx never carried a `text-red-800` block, so this worker's own test
  asserts PanelError-import on the three files that needed it and `buttonClass`-import on StatusPanel.tsx
  instead, recorded rather than silently narrowed.

## Rows filed

- `IRPT_FNTEND-W17-S1` -- DrillTree `:234` structurally unreachable (adapter derives both comparison sides
  from one expression). OBSERVATION / INERT.
- `IRPT_FNTEND-W17-S2` -- F67-AC10's literal invocation crashes; the adapted, substance-proving run's own
  output never matches `<expect>SAVED|scrollLeft</expect>`. OBSERVATION / INERT.
- `IRPT_FNTEND-W17-S3` -- F67-AC3's control fixture (`default.json`) is missing `unprojected_grant` on
  every entry, causing a genuine (unrelated) EnvelopeMismatch; root cause confirmed by a positive-control
  patch. OBSERVATION / INERT.
- `IRPT_FNTEND-W17-S4` -- the cell text's literal "PanelError imported by all four files" would add an
  unused import to StatusPanel.tsx; resolved by judgment, recorded rather than silently narrowed.
  OBSERVATION / INERT.
- `IRPT_FNTEND-W17-S5` -- filed AFTER the COO's first amendment (`5cad85da0b`) landed and was applied to
  this worktree: that amendment's corrected F67-AC10 `<invocation>` text contained a non-declared,
  non-executable bracketed span, so `proof-of-spec-check.py`'s ENFORCE-mode invocation-alignment limb
  refused any real command recorded against it (1 violation, `INVALID` rc=1) even though the criterion's
  substantive `<expect>DRIVER OK</expect>` was independently re-verified PASS. RESOLVED by a SECOND
  amendment (`b570ecf546`, see below): `<invocation>` now points at this worker's own already-authored,
  already-committed scenario-map file, a real literal command. OBSERVATION / INERT (row stays filed as the
  record; not edited).

## Amendments applied mid-task (COO commits `5cad85da0b`, `b570ecf546`)

**First amendment (`5cad85da0b`).** Verified independently before use: `git cat-file -t 5cad85da0b` ->
`commit`; `git show --name-only 5cad85da0b` -> exactly one path, the governing task-order file; the diff
against its parent read directly and matched, word for word, what the coordinator's message described (two
`COO AMENDMENT` blocks, after F67-AC3 and after F67-AC10). Applied as a working-tree edit to this worker's
own copy of the TO (this worker's branch does not track CLOUD); `diff --strip-trailing-cr` against `git
show 5cad85da0b:<path>` afterward returned 0 lines -- content-identical. F67-AC3 re-verified PASS (fixture
swap). F67-AC10's `<expect>` re-verified PASS (`DRIVER OK`); its `<invocation>` text itself carried a
residual defect (row `IRPT_FNTEND-W17-S5`) that kept the whole proof-of-spec-check instance `INVALID
(rc=1)`.

**Second amendment (`b570ecf546`).** Verified the same way: `git cat-file -t` resolves, `git show
--name-only` touches ONLY the TO file, diff read directly confirming the `<invocation>` now points at this
worker's own already-committed `f67_overflow_scenarios.json` using only the declared `WS`/`PORT`
placeholders. Applied to this worker's own worktree copy; `diff --strip-trailing-cr` against `git show
b570ecf546:<path>` afterward: 0 lines. Re-ran `proof-of-spec-check.py`: `invocation-alignment 11/11 match,
0 diverge`, `violations=0`, **`VALID (rc=0)`**, all 12 criteria PASS or RECORDED (judgment). **`<status>`
FLIPPED TO `complete`, this tick.**

## Push state

LOCAL only. Workspace branch `wk-irpt_fntend-11-67-fe-s-67`, portal branch
`wk-irpt_fntend-11-67-fe-s-67-portal`. Never pushed, merged, rebased or `checkout --`'d against the shared
tree. PORTAL IS FROZEN per BOUNDS.
