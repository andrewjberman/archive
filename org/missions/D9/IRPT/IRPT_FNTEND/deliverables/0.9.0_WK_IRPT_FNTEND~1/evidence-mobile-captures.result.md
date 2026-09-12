# IRPT_FNTEND.TO-FE-s-18 -- evidence, mobile captures, Lato Bold, R3 re-pin

`0.9.0_WK_IRPT_FNTEND~1` | workspace branch `wk-irpt_fntend-2-7-fe-s-18` (cut from CLOUD @7b04394dcb) |
portal branch `wk-irpt_fntend-2-7-fe-s-18` (cut from DEV @774c595b) | dev server `bun run dev --port 5181`,
started once from the portal worktree and killed before this report (`netstat` on 5181 reads 0 listeners).
**Push state: LOCAL in both repos. Portal is FROZEN; nothing was pushed, merged, rebased, checked out or cleaned.**

## THE HEADLINE, BEFORE THE DETAIL

**Two criteria are REFUSED and the order stays open.**

- **F18-AC3** -- `no two entries share a file or a hash` is FALSE. The three Holdings captures are
  BYTE-IDENTICAL (sha256 `8ce52e6ad0b60e29...`). Row `IRPT_FNTEND-W1-S34`.
- **F18-AC17** -- `bun test src/pages/InvestorReporting` reads **420 pass / 1 skip / 1 fail**. The one
  failure is F18-AC3's own arm, deliberately not softened. Same row.
- **F18-AC6** -- the print URL the criterion specifies refuses before the network; run as written and
  recorded, with a CONTROL run that resolves. See its row in the table.

**And the reason three captures are one picture is the biggest thing this order found.**
At this commit the **Reporting and Holdings tab BODIES cannot mount from any network response.**
Both gate on `envelopeFromAvailability(payload.availability).state`, and NO document adapter in
`contracts/adapt.ts` ever sets `state`, so `wireEnvelope`'s default `EXPLICIT_UNKNOWN_STATE = 'UNCERTAIN'`
is what every response yields. The v1 envelope's REAL state is parsed (`contracts/envelope.ts:193`) and then
discarded by the client (`api/endpoints/investor-reporting.ts:932` returns `parsed.data` only). Every
tab-body test seeds the component directly (`initialReport` / `initialSnapshot` / `initialEnvelope`), so the
suite reads green while the only path the product uses is dead. Round-1's own captures
(`fe-s-11_holdings_390.png`, `fe-s-5_reporting_49f_1440.png`) show both bodies rendering, so this is a
REGRESSION that arrived with the v1 envelope plane. Row **`IRPT_FNTEND-W1-S33`**, class BLOCKING, ARMED.
The fix is outside this order's grant in every direction.

## CRITERIA

| id | verdict | invocation (abridged; each was run exactly as the face wrote it) | deciding output |
|---|---|---|---|
| F18-AC1 | PASS | `bun run typecheck` | `$ tsc -b --noEmit` then `rc=0` |
| F18-AC2 | PASS | `bun test __tests__/fe-s-18/paired.test.ts` | `PAIRED: 1 report, 3 views` (3 pass, 0 fail) |
| F18-AC3 | **FAIL** | `bun test __tests__/fe-s-18/manifest.test.ts` | `MANIFEST: 12 entries`, `UNIQUE FILES: ok`, then `DISTINCT HASHES: 10 of 12` + `COLLIDING SETS: 1`; 4 pass, **1 fail** |
| F18-AC4 | PASS | `ui-smoke ... --width 390 --fixtures fe-s-18-frozen.json --click Reporting` | `CLICKED: Reporting`, `FIXTURES: 9 declared; 3 matched >=1 URL`, rc=0 |
| F18-AC5 | PASS | `ui-smoke ... --width 1440 --fixtures fe-s-18-frozen.json --click Export` | `CLICKED: Export`, `FIXTURES: 9 declared; 3 matched >=1 URL`, rc=0 |
| F18-AC6 | **FAIL (refused)** | `ui-smoke "investor-reporting/print?bundle=fe-s-18-frozen" ... --console "REFS RESOLVED"` | NO `REFS RESOLVED` line. Page text: `This bundle was not rendered ... cannot render reportKind 'performance-report': fe-s-18-frozen is absent`; `FIXTURES: 9 declared; 0 matched >=1 URL`; rc=0 |
| F18-AC7 | PASS | `ui-smoke ... --width 390 --fixtures fe-s-15-clean.json --click Analysis` | `CLICKED: Analysis`, `FIXTURES: 5 declared; 3 matched`, rc=0 |
| F18-AC8 | PASS | `ui-smoke ... --fixtures fe-s-15-needs-correction.json --click Analysis` | `CLICKED: Analysis`, `FIXTURES: 5 declared; 3 matched`, rc=0 |
| F18-AC9 | PASS (bar) | `ui-smoke ... --fixtures fe-s-18-holdings-observed.json --click Holdings` | `CLICKED: Holdings`, `FIXTURES: 9 declared; 3 matched`, rc=0 |
| F18-AC10 | PASS (bar) | `ui-smoke ... --fixtures fe-s-18-holdings-target.json --click Holdings` | `CLICKED: Holdings`, `FIXTURES: 9 declared; 3 matched`, rc=0 |
| F18-AC11 | PASS (bar) | `ui-smoke ... --fixtures fe-s-18-holdings-missing-attribution.json --click Holdings` | `CLICKED: Holdings`, `FIXTURES: 9 declared; 3 matched`, rc=0 |
| F18-AC12 | PASS | `ui-smoke "print?bundle=fe-s-16-narrative&narrative=1&tenant=F-49F&scope=fp-49f-0824&revision=rev-49f-000091"` | `CONSOLE[log]: REFS RESOLVED: 1 of 1`, `FIXTURES: 2 declared; 2 matched`, rc=0 |
| F18-AC13 | PASS | same shape, `bundle=fe-s-16-prehistory` | `CONSOLE[log]: REFS RESOLVED: 1 of 1`, `FIXTURES: 2 declared; 2 matched`, rc=0 |
| F18-AC14 | PASS | `ui-smoke ... --width 1440 --fixtures fe-s-14-global.json --click Holdings` | `CLICKED: Holdings`, `FIXTURES: 2 declared; 2 matched`, rc=0 |
| F18-AC15 | PASS | `bun run .../census.ts` | `COMPONENTS: 70 (REUSED 27, NEW 43)`, `SCANNED: 40 tree files + src/App.tsx`, `DEFINED-BUT-NOT-IMPORTED: 0`, `PRD-REUSE-ROWS: 11 of 11 accounted`, rc=0 |
| F18-AC16 | PASS | `bun test __tests__/fe-s-11/colour-law.test.ts` | `SCANNED: 40 files`, 4 pass, `0 fail` |
| F18-AC17 | **FAIL** | `bun test src/pages/InvestorReporting` | `420 pass`, `1 skip`, **`1 fail`**, 422 tests across 69 files |
| F18-AC18 | RECORDED (judgment) | -- | no verdict taken; see "FOR THE L9 READ" below |
| F18-AC19 | PASS | `bun test __tests__/fe-s-17/fonts.test.ts` | `FONTS: 4 of 4`; `BOLD ON DISK: Lato-Bold.ttf bytes=656544 sha256=8a0aace75d33794eece4b28187bfc1df0bbd2888b5d8a56e01788c8d65d16be1`; 11 pass, 0 fail |
| F18-AC20 | PASS | same run | `STAND-INS: 0`; `NOT PACKAGED (manifest.ts): italic`; `FACES CHECKED: 4; WEIGHT MISMATCHES: 0` |

**"PASS (bar)" on AC9/AC10/AC11 is deliberate wording and is not a hedge.** Each printed its expected
`CLICKED: Holdings` and each produced a real PNG, so the criterion's stated bar is met by output. What the
PNGs show is StatusPanel "Uncertain", not the observed / target / missing-attribution bases the criteria
name. `IRPT_FNTEND-W1-S33` carries that, the manifest says it on each of those three rows, and F18-AC3's
failure is the mechanical consequence. **F18-AC4 is the same shape** and its manifest row says so too.

### F18-AC6, in full

Run as written (no `&scope=`, no `&revision=`), recorded verbatim above, PNG saved as
`fe-s-18_print_frozen_1440.png` -- the refusal panel, which `PrintEntry.tsx`'s own header requires to be
DISPLAYED rather than blank. Since FE-s-14 the declared performance route binds the scope fingerprint as a
PATH parameter (row `IRPT_FNTEND-W2-S13`), so the request cannot be built and the refusal happens before the
network: `FIXTURES: 9 declared; 0 matched >=1 URL`.

**CONTROL, same commit, same fixture map, same bundle id, with `&tenant=F-49F&scope=fp-49f-0824&revision=rev-49f-000091`
added:** `CONSOLE[log]: REFS RESOLVED: 1 of 1`, `FIXTURES: 9 declared; 1 matched >=1 URL`, and the frozen
report renders in full. Saved as `fe-s-18_print_frozen_control_1440.png` and carried in the manifest as
`F18-AC6 (CONTROL)`. **The page is not at fault; the criterion's URL is.** The fix is four query params in
the criterion, and it belongs to the issuer, not to this worker.

## R3 -- THE RE-PIN, DONE FIRST, BEFORE ANY CAPTURE

**Vintage:** `git log -1 --format=%h -- docs/contracts/investor-reporting/v1` = **`b8e98d5a4d`** in this
worktree. That is the artifact everything below is pinned to.

Before: `bun test src/pages/InvestorReporting/__tests__/fe-s-13` printed
`STALE PINS: AnalysisReport: pinned 6fa8a991abfe, on disk add2aaf1f0cb` and
`StatusEnvelope: pinned cdcd91b44cf3, on disk 9c4bcce436bf`, `WIRE SCHEMA PINS FRESH: 9 of 11`, 27 pass 1 fail.

- `fixtures/wire/` copies needed **nothing**: `FIXTURE COPIES IDENTICAL: 11 of 11` before and after. The
  face's `4 stale fixture copies` does not reproduce -- it was TWO stale schema pins, and the `4` is bun's
  `Received + 4` DIFF-LINE count. Row `IRPT_FNTEND-W1-S27`.
- The wire types were regenerated with the project's own generator. `AnalysisReport.ts` gained
  `readonly date_claim?: 'SECTION' | 'REPORT' | 'NONE'`; `StatusEnvelope.ts`'s `source_dates.business_date`
  became OPTIONAL (the state-conditional obligation has no TypeScript form -- optional is the safe
  direction for a consumer and enforcement stays the producer's); `index.ts` took the two new pins.
  Ten other generated files are byte-identical.
- **The generator had to be repaired first.** Run unmodified it emitted the literal
  `export interface StatusEnvelopeWire unknown` -- `renderType` tests `allOf` BEFORE `type`/`properties`, and
  StatusEnvelope now carries both, so a shapeless `if`/`then` member replaced the whole object body. A
  `carriesShape` predicate now skips shapeless members and falls through. The twelve response schemas that
  use `allOf` legitimately regenerate byte-identically before and after. Row `IRPT_FNTEND-W1-S26`.

After: `28 pass, 0 fail`, `WIRE SCHEMA PINS FRESH: 11 of 11`, `RESPONSE SCHEMA PINS FRESH: 12 of 12`,
`FIXTURE COPIES IDENTICAL: 11 of 11`. `bun run typecheck` rc=0.

## LATO BOLD

Copied byte for byte from `/c/Users/AndrewBerman/Desktop/ajb_workspace/.runtime/codex-seats/4.0.0_SA_CRO/performance-export-recon/fonts/Lato-Bold.ttf`
(`cmp` reports the two identical; `sha256sum` on the copy returns
`8a0aace75d33794eece4b28187bfc1df0bbd2888b5d8a56e01788c8d65d16be1`, 656544 bytes -- the issuer's published
values). **Nothing was fetched by this worker.**

- `render/assets/fonts/Lato-Bold.ttf` added; `fonts.manifest.json` gains its entry (weight 700, style
  normal, licence OFL-1.1), `stand_ins` is now `{}` and `not_packaged` is exactly `["italic"]`.
- `render/print.css`: the 700 face names `Lato-Bold.ttf` and the stand-in comment is gone.
- **A 600 `@font-face` had to be ADDED, and this is the non-obvious part.** print.css sets
  `font-weight: 600` in **EIGHT** rules (counted at HEAD with `git show HEAD:...print.css | grep -c`) and
  declared NO 600 face: those rules matched UP to 700, which was itself the SemiBold FILE standing in. So
  600 text rendered in SemiBold through two substitutions that cancelled. Pointing 700 at the real Bold
  breaks the cancellation and would have re-weighted all eight to true Bold with nothing in the diff saying
  so. The only thing that objected was FE-s-17's own "each packaged face is pointed at by at least one rule"
  claim, which failed on the orphaned SemiBold. Row `IRPT_FNTEND-W1-S29`; its cardinality correction is
  `IRPT_FNTEND-W1-S32`.
- `render/manifest.ts`: `fontPackage.files` gains the Bold row, `standIns: {}`, `notPackaged: ['italic']`.
  **`RENDER_PACKAGE.fonts` stays at THREE names.** `__tests__/fe-s-4/manifest.test.ts:216` asserts
  `length === 3` and fe-s-4 is outside this grant; the order's own fallback clause was taken. Row
  `IRPT_FNTEND-W1-S28` (ARMED). The flat list now carries a WARN block naming `fontPackage.files` as the
  complete one, and `fonts.test.ts` asserts the shortfall explicitly instead of asserting an equality that
  is no longer true.
- `__tests__/fe-s-17/fonts.test.ts` was **NOT** already updated, contrary to the face; this worker wrote the
  update. Row `IRPT_FNTEND-W1-S30`, which also discloses that F18-AC19/AC20 grade output from a test
  authored in the same order that is graded by it.
- The Bold is not listed in the capture directory's `sources.json` (four entries: Regular, Light, SemiBold,
  OFL.txt), so its per-face `source` diverges from the manifest-level one and the test now prints
  `DISTINCT FACE SOURCES: 2 across 4 face(s); 3 from the manifest-level source`. Row `IRPT_FNTEND-W1-S31`.

## LAYOUT EDITS -- EVERY ONE, BY FILE AND LINE

All are class attributes, wrappers or order of siblings. **No prop, state, data read, adapter call or text
was changed.** The 1440 layout is unmoved: `fe-s-18_global_two_firms_1440.png` is the control, and its tab
strip matches round-1's captures.

| file | line(s) | edit | why |
|---|---|---|---|
| `tabs/TabShell.tsx` | 167-190 | `overflow-x-auto` wrapper + a responsive `className` passed to the shared `TabNavigation`: `mx-0 px-2 [&_button]:gap-1 [&_button]:px-1 [&_button]:text-xs [&_button]:tracking-normal sm:-mx-8 sm:px-8 sm:[&_button]:gap-2.5 sm:[&_button]:px-4 sm:[&_button]:text-sm sm:[&_button]:tracking-wider` | At 390 HOLDINGS ran off the right edge, cut and unreachable. THE CAUSE WAS NOT THE LABELS: `TabNavigation` carries `-mx-8 px-8` so its sticky background can bleed to the page edges, making the strip 64px WIDER than its container BY DESIGN. `cn` is `tailwind-merge`, so the `sm:` half restores the exact original pair at >=640px. `TabNavigation` itself is outside the grant and is imported unchanged. |
| `tabs/reporting/PeriodControls.tsx` | 69-73, 78, 87 | `flex` -> `flex flex-wrap` on the custom-range label; `min-w-0` on both date inputs | The second date input and the `to` separator ran past the white card at 390. |
| `tabs/reporting/PeriodControls.tsx` | 101-113 | date-window `div` -> `flex flex-wrap gap-x-3 gap-y-1`; each window statement `whitespace-nowrap`; the two `ml-3` margins removed (the gap replaces them) | As one inline paragraph it broke each window MID-DATE (`2026-09-` / `12`), which reads as a different date. |
| `tabs/holdings/SliceTable.tsx` | 47-51 | `w-full` -> `w-full min-w-[640px]` | The wrapper already had `overflow-x-auto`, but `w-full` ALONE told the table to shrink to the container, so nine columns squeezed and the last ones clipped rather than scrolling. This is what makes the existing scroll container do anything. |
| `tabs/holdings/HoldingsTab.tsx` | 99-112 | the firm chip gets its OWN right-aligned row above the summary card; the card is no longer a flex sibling of it | They shared one non-wrapping flex row: the chip sat outside the white card and was clipped at 390 while the card was squeezed to ~300px. This is the arrangement `ReportingTab` already uses for the same component. |
| `tabs/holdings/HoldingsSummary.tsx` | 53-61 | `p-6 grid grid-cols-2 sm:grid-cols-4` -> `p-4 sm:p-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4` | At 390 each cell got ~150px, so "Unique accounts" wrapped to two lines and its large value collided with the second line. At >=768px the four-column card is unchanged. |

**NOT DONE, and named rather than worked around: the pie labels.** The clipping comes from recharts'
`outerRadius={100}` and a label callback drawing `name: value` outside the arc; `overflow-x-auto` cannot
reach it because `ResponsiveContainer` sizes itself to its parent. Both are PROPS, which BOUNDS excludes by
name. Row `IRPT_FNTEND-W1-S35`.

**OBSERVED AND LEFT:** the export modal's preview renders a letter-landscape document inside a `2xl` panel
and scrolls it horizontally (`ExportModal.tsx`, `data-slot="preview-scroll"`). That is FE-s-16's stated,
commented decision, so a still capture showing its left portion is the instrument, not a defect.

**FOUR of the six layout repairs are verified by capture. Two are not**, because they live in the Holdings
body, which does not mount (`IRPT_FNTEND-W1-S33`): the summary card and the slice table. They were made
against round-1's `fe-s-11_holdings_390.png`, which DOES show the body and shows both defects. They are
correct by construction and unproven by this order's evidence, and that sentence is the honest one.

## FIXTURES ADDED

Generated by `__tests__/fe-s-18/gen-fixtures.ts` (committed; it is the record of how each was derived), never
hand-typed:

- `fe-s-18-frozen.json` -- all nine v1 route keys from `fe-s-13-wire.json`, with ONE performance body taken
  from `fe-s-16-print-narrative.json` (the one body MEASURED to render all four print pages), frozen at
  `source_revision bd-2026-09-09` / `calculation_id calc-rev-49f-000091`, with a nine-point series, three
  summary returns (one of them `absent_reason: NOT_ENOUGH_HISTORY`) and two accounts.
- `fe-s-18-holdings-{observed,target,missing-attribution}.json` -- the same three-node tree (Models 3.00M /
  SMA 1.20M / Client 800K of a 5.00M unique custody total) differing in EXACTLY one thing each, so a reader
  comparing captures is looking at one difference. `missing-attribution` omits `classification` entirely,
  which the schema permits (the node's own `required` list is node_id, level, node_kind, basis, amount,
  percentages, provenance -- read from the schema, not remembered); an empty object would have been a
  different claim and would not validate.
- `fe-s-16-print-prehistory.json` -- **built here because FE-s-16 left none**, from FE-s-16's own bun fixture
  `__tests__/fe-s-16/fe-s-16-narrative-pre-history.wire.json` wrapped in a v1 envelope, beside the same
  performance body F18-AC12 uses. F18-AC13 instructs exactly this and instructs saying so.

## CENSUS

`COMPONENTS: 70 (REUSED 27, NEW 43)` across 40 scanned tree files plus `src/App.tsx`;
`DEFINED-BUT-NOT-IMPORTED: 0`; `PRD-REUSE-ROWS: 11 of 11 accounted`. **NEW rows without a reason: 0 of 43**
(checked by reading `component-census.json` and counting empty reason fields, not by eye), so no surprise row
is owed on that clause. Both census outputs were overwritten in place as the order directs.

## FOR THE L9 READ (F18-AC18 -- RECORDED, NO VERDICT)

Three things the grader needs that the images do not carry:

1. **Four of the twelve captures show StatusPanel "Uncertain" where the criterion names a report or a
   holdings basis** (AC4, AC9, AC10, AC11). Not a rendering defect of the layout work -- the body never
   mounts. `IRPT_FNTEND-W1-S33`.
2. **The frozen-report pair that CAN be compared is preview vs print:** `fe-s-18_preview_frozen_1440.png`
   and `fe-s-18_print_frozen_control_1440.png`, both from `fe-s-18-frozen.json`, whose single
   performance-report body hashes to `9c8b821b4aeb1763...` for all three views (F18-AC2 prints it). The
   SCREEN third of that pair is the one the gate blanks.
3. **The print captures carry the real Bold**, and every `font-weight: 600` rule in them is served by
   SemiBold rather than by Bold only because the 600 face was added in the same commit.

## SURPRISE ROWS FILED (10)

`IRPT_FNTEND-W1-S26` OBSERVATION/INERT -- gen-wire.ts's `allOf` branch shadows an object body.
`IRPT_FNTEND-W1-S27` OBSERVATION/INERT -- the R3 premise's `4 stale fixture copies` is 2 stale schema pins.
`IRPT_FNTEND-W1-S28` OBSERVATION/**ARMED** (disarm `2.0.0_SA_COO~F`) -- `RENDER_PACKAGE.fonts` cannot take the 4th name inside this grant.
`IRPT_FNTEND-W1-S29` OBSERVATION/INERT -- eight `font-weight: 600` rules had no 600 face and were served by the 700 stand-in.
`IRPT_FNTEND-W1-S30` OBSERVATION/INERT -- fonts.test.ts was not already updated; AC19/AC20 grade a test written in this order.
`IRPT_FNTEND-W1-S31` OBSERVATION/INERT -- the Bold is absent from the capture's `sources.json`; per-face provenance diverges.
`IRPT_FNTEND-W1-S32` OBSERVATION/INERT -- correction to this worker's own S29: EIGHT rules, not nine, and S29's line numbers are working-copy ones.
`IRPT_FNTEND-W1-S33` **BLOCKING**/**ARMED** (disarm `2.0.0_SA_COO~F`) -- the Reporting and Holdings tab bodies cannot mount from any network response.
`IRPT_FNTEND-W1-S34` **BLOCKING**/INERT -- F18-AC3 and F18-AC17 refused; three captures byte-identical.
`IRPT_FNTEND-W1-S35` OBSERVATION/INERT -- the pie-label repair needs a prop change that LAYOUT ONLY excludes.

## HOUSEKEEPING

Ten files under `contracts/wire/` show as modified in `git status` with `git diff --numstat` reporting NO
lines changed -- the generator writes LF and the worktree is `autocrlf`. They are **not staged**; only the
three files with real content changes (`AnalysisReport.ts`, `StatusEnvelope.ts`, `index.ts`) are. Nothing was
`checkout --`ed or cleaned to tidy this, per the standing prohibition.


---

# ADDENDUM -- THE ISSUER AMENDMENT (74cefaf7a2, rows IRPT_FNTEND-S30 and S31)

A short pass, on the issuer's instruction: **re-run F18-AC6 and F18-AC3, update the instance, do not re-run
anything else, do not flip `<status>`.** Everything above stands unless contradicted here.

## Re-grounding, before re-running

`74cefaf7a2` is reachable from this worktree (linked worktrees share the object database), so the amended
invocation was read **from the file at the commit** rather than trusted from the message:
`git show 74cefaf7a2:org/.../IRPT_FNTEND.TO-FE-s-18.evidence-mobile-captures.md` line 59 carries the new
F18-AC6 invocation character for character as the issuer stated it, `&narrative=0` included, with
`<expect>REFS RESOLVED: 1 of 1</expect>` unchanged. **My branch was cut at `7b04394dcb`, before the
amendment, so the task-order file IN THIS WORKTREE still carries the pre-amendment URL.** The run below used
the AMENDED invocation. That divergence is stated rather than glossed: the record's authority is the file at
`74cefaf7a2`, not the copy on this branch.

Lines 77 and 80 of the same file now carry the F18-AC12 and F18-AC13 URLs I had already run (the issuer's
own `IRPT_FNTEND-S31` records that those corrections had reached my spawn prompt but not the file). Neither
was re-run, per instruction.

## F18-AC6 -- NOW PASSES

Invocation, exactly as amended:

    cd /c/tmp/wk-irpt_fntend-2-7-fe-s-18/portal && timeout 120 node scripts/ui-smoke.mjs \
      "investor-reporting/print?bundle=fe-s-18-frozen&narrative=0&tenant=F-49F&scope=fp-49f-0824&revision=rev-49f-000091" \
      <deliverables>/fe-s-18_print_frozen_1440.png --port 5181 --width 1440 \
      --fixtures src/pages/InvestorReporting/fixtures/smoke/fe-s-18-frozen.json --console "REFS RESOLVED"; echo rc=$?

Output: `CONSOLE[log]: REFS RESOLVED: 1 of 1` (twice), `VIEWPORT: 1440x900`,
`FIXTURES: 9 declared; 1 matched >=1 URL`, `rc=0`. **PASS.**

The PNG at `fe-s-18_print_frozen_1440.png` **replaced** the refusal image under the same filename: it is now
the frozen report printed in full over three pages -- the nine-point cumulative series, the three summary
returns including the `UNAVAILABLE (NOT_ENOUGH_HISTORY)` 3Y row, both accounts, and the Methods and Sources
page. Its figures match `fe-s-18_preview_frozen_1440.png` (both read `2026-01-02 to 2026-09-09`,
`rev-49f-000091`), so **the preview/print half of F18-AC18's pair is now a real comparison.**

**WHICH FILE IS WHICH, since two now resolve:**

- `fe-s-18_print_frozen_1440.png` -- **the criterion's capture**, from the amended invocation.
- `fe-s-18_print_frozen_control_1440.png` -- **kept, and not a criterion capture.** It is the control run
  from the refusal pass, the thing that localised the fault to the URL and the evidence the amendment was
  made on. It differs from the criterion capture only in carrying no `&narrative=0`.

## F18-AC3 -- RE-MEASURED, STILL FAILS, AND ITS RULE IS NOW THE RIGHT ONE

The AC6 re-capture changed that file's bytes, so the manifest was rebuilt and the test re-run. It reads:

    MANIFEST: 12 entries / MISSING FILES: 0 / DRIFTED HASHES: 0 / FIELDS COMPLETE: 12 of 12 entries
    DISTINCT FILES: 12 of 12 / UNIQUE FILES: ok
    DISTINCT HASHES: 9 of 12
      BYTE-IDENTICAL CAPTURES (f125df3b33388a1b): fe-s-18_print_frozen_1440.png, fe-s-18_print_frozen_control_1440.png
        1 distinct fixture(s) -> EXPECTED-BY-CONSTRUCTION -- one fixture, one render
      BYTE-IDENTICAL CAPTURES (8ce52e6ad0b60e29): fe-s-18_holdings_observed_390.png, fe-s-18_holdings_target_390.png, fe-s-18_holdings_missing_attribution_390.png
        3 distinct fixture(s) -> UNEXPECTED -- different fixtures, identical pixels
    COLLIDING SETS: 2; UNEXPECTED COLLISIONS: 1
    4 pass, 1 fail

**A SECOND COLLISION APPEARED AND IT IS NOT A DEFECT.** The amended F18-AC6 capture is byte-identical to its
own control: `&narrative=0` is the package default, so the two URLs request the identical render. A flat
"no two entries share a hash" assertion would have counted that as a second failure and buried the real one
underneath it.

So the arm was re-scoped to **the rule the issuer is carrying to L10 -- a capture set asserts DISTINCT HASHES
*whenever its fixtures differ*.** The classification is computed from the manifest's own `fixture` field,
never from a list of filenames, so it cannot absorb a defect: any future collision across different fixtures
still fails. Under it the Holdings three still FAIL, which is the point.

**This is a narrowing of the arm and it is disclosed as one.** Under the criterion's literal prose
("no two entries share a file or a hash") the AC6/control pair is also a violation; under the rule the
prose is trying to express, it is not. I applied the second reading and printed both, so a grader can take
either. **F18-AC3 remains FAIL either way**, and the reason is unchanged: three fixtures, one picture,
`IRPT_FNTEND-W1-S33`.

## F18-AC17 -- NOT RE-RUN, and what is therefore claimed about it

Per instruction. Its recorded output (`420 pass, 1 skip, 1 fail` across 422 tests in 69 files) predates the
AC6 re-run. What **was** measured just now is the only file that changed: `manifest.test.ts` still has 5
tests and still reads 4 pass / 1 fail, on the same single arm. The suite totals therefore do not move, and
that sentence is an inference from a direct measurement of the changed file, **not** a re-run of the suite.

## Rows added in this pass

`IRPT_FNTEND-W1-S36` OBSERVATION/INERT -- `ui-smoke.mjs:341` compares `window.location.pathname` against the
full route STRING, so `<-- DID NOT LAND (auth redirect? bad route?)` prints on **every** query-bearing route
whether or not anything went wrong. Observed on the AC6 run that landed and rendered three pages. Five of
this order's twelve captures use query-bearing routes, so the round's evidence carries an alarming line that
means nothing; no criterion turns on it (`REFS RESOLVED` is the real oracle). `scripts/ui-smoke.mjs` is
outside this order's `<paths>`, so it is named and not edited.

## What did NOT change

`<status>` stays `pending`. F18-AC3 and F18-AC17 remain FAIL and the order stays open -- the issuer has
confirmed both are true failures reporting `IRPT_FNTEND-W1-S33` and is deliberately not amending them.
No other criterion was re-run. `RENDER_PACKAGE.fonts` is left at three names (`W1-S28`), as instructed.
Portal remains FROZEN; both commits are LOCAL.


---

# ADDENDUM 2 -- THE ISSUER RULING ON F18-AC3's ARM

**The narrowing recorded in Addendum 1 is REVERTED.** `2.0.0_SA_COO~F` ruled that F18-AC3's prose --
*no two entries share a file or a hash* -- is correct as written and stays, and that the fault was never in
the arm: **it was that the control had been made a manifest entry at all.**

The ruling names the criterion's own first clause as the test of what belongs in the population: *"every PNG
**this order names** exists under the deliverables folder"*. **Eleven criteria name a capture** -- F18-AC4,
AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14. `fe-s-18_print_frozen_control_1440.png` is named by
none of them. It is PROVENANCE for the S31 amendment, not evidence for a bar.

The issuer also recorded that the narrowing traced to its own message rather than to my reading: the
"fixtures differ" formulation arrived as a standing rule being carried to L10, which is a recommendation and
not law until the CTO rules it, and a criterion patched through a message is a defective face. I am
recording that here because the instance's earlier FAIL reason attributed the rule to the issuer without
saying it had no standing yet.

## What changed

1. **The arm is back to the literal rule** -- no two manifest entries share a file or a hash. The
   fixtures-differ classification and the `UNEXPECTED COLLISIONS` line are gone with it. One rule, as cut.
   The test's comment now carries the whole history so the next reader does not re-derive the wrong repair.
2. **`captures.manifest.json` is rebuilt over the eleven criterion captures only.** `entry_count` is 11.
3. **The control file stays on disk and is not lost by leaving the manifest.** Recorded here:

   | file | sha256 | what it is |
   |---|---|---|
   | `fe-s-18_print_frozen_control_1440.png` | `f125df3b33388a1b9962acb42f64b7c22bd707a3b846b21326320ff65344d277` | **NOT A CRITERION CAPTURE.** The control run from the refusal pass: `investor-reporting/print?bundle=fe-s-18-frozen&tenant=F-49F&scope=fp-49f-0824&revision=rev-49f-000091`, which printed `REFS RESOLVED: 1 of 1` while the criterion's own URL refused. It is what localised the fault to the URL and is the evidence the F18-AC6 amendment (`74cefaf7a2`, row `IRPT_FNTEND-S31`) was made on. It is byte-identical to the amended F18-AC6 capture, because `&narrative=0` is the package default. |

   **Twelve PNGs are on disk; eleven are manifest entries.** That difference is deliberate and is stated in
   the manifest's own `population` field as well as here.

## F18-AC3 -- re-run under the restored rule, STILL FAILS

    MANIFEST: 11 entries / MISSING FILES: 0 / DRIFTED HASHES: 0 / FIELDS COMPLETE: 11 of 11 entries
    DISTINCT FILES: 11 of 11 / UNIQUE FILES: ok
    DISTINCT HASHES: 9 of 11
      BYTE-IDENTICAL CAPTURES (8ce52e6ad0b60e29): fe-s-18_holdings_observed_390.png, fe-s-18_holdings_target_390.png, fe-s-18_holdings_missing_attribution_390.png
    COLLIDING SETS: 1
    4 pass, 1 fail

**One colliding set, and it is the real defect.** The criterion is unweakened and the signal is clean --
which is the outcome the narrowing was reaching for and did not deserve to reach by moving the bar. Three
fixtures, one picture, `IRPT_FNTEND-W1-S33`.

## Unchanged

`<status>` stays `pending`. F18-AC17 remains FAIL and was not re-run (the only file that changed,
`manifest.test.ts`, still reads 4 pass / 1 fail on the same single arm). F18-AC6 remains PASS on the amended
invocation. No capture was re-taken in this pass -- no dev server was started, and the eleven PNG bytes are
untouched, which the manifest's own `DRIFTED HASHES: 0` re-confirms against the files on disk.
