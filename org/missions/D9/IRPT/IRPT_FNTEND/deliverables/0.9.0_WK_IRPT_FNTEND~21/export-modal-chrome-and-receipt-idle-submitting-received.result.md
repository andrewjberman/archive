# Result -- IRPT_FNTEND.TO-FE-s-71 (0.9.0_WK_IRPT_FNTEND~21)

**These captures are FIXTURE-FED.** Every PNG and every EXPECT/ASSERT/FIXTURES-MATCH line below
was produced by `scripts/ui-smoke.mjs` driving the REAL `/investor-reporting` route against the
worktree's own dev server (port 5963), with the network layer answered by a static fixture map
(`--fixtures ...`) -- no live backend was reached, and no route was mocked at the React level. This
is the right evidence for FWD-12's card here: the cell fixes CHROME (colour/shape/weight law) and a
CLIENT-SIDE flow-state distinction (row S69) that render identically regardless of which real backend
answered the request -- what matters is that the REAL modal component, REAL Panel component and REAL
ReceiptPanel component render this way on the REAL route, not what data populated the numbers. It is
NOT the right evidence for the other seven FWD-12 cards this round, each of which is about a specific
tab's real-data behaviour and needs its own real-route half.

## THE FIXES (cited to clause)

- **C3** -- `export/ExportModal.tsx`'s modal-body `<Panel variant="chart">` (resolves to the BAND,
  `#0A1733`, nested inside the light dialog sheet -- C3's own definition of the defect) is now
  `<Panel variant="nested">`, confirmed an EXISTING variant by reading `Panel.tsx`'s own decision-tree
  comment before relying on it: `nested: 'bg-[hsl(var(--bg-surface))]'` i.e. `--bg-surface` `#FFFFFF`,
  "DARK text only". Every light-on-dark class this region carried (the Branding legend, the three chip
  labels, `no-approved-assets`, the narrative-toggle text + its "unavailable" span, the account-detail
  label, the optional-sections legend + its item labels) is flipped to navy-on-white (`text-slate-900`
  / `text-slate-500` / `text-slate-400`, matching the idiom `AppliedBranding.tsx`/`ReceiptPanel.tsx`
  already used) per DESIGN.md's inversion rule (C5). The separate `rounded-md bg-white p-3` light-card
  wrapper FE-s-16 built around `AppliedBranding`/`ReceiptPanel` for the OLD dark panel is retired (the
  Panel itself is now the white surface those two components were always written canvas-legal for).
- **C8** -- the selected branding chip now takes the SAME weight-and-rule idiom FE-s-61 already used
  for `PeriodControls`'s period presets: `font-bold border-2 border-[#163372] bg-white text-[#163372]`
  when selected, `font-normal border border-slate-300 bg-white text-slate-900` when available-but-
  unselected, `font-normal border border-slate-200 bg-slate-100 text-slate-400` when unavailable --
  never a second filled-purple chip. `aria-pressed` is added to each chip so the selected state is
  selector-addressable (F71-AC10). `Close` is demoted to a plain/bordered button
  (`border border-[#163372] bg-white text-[#163372]`, `data-slot="close"` added), never a second
  filled-primary beside `Create export`.
- **C11** -- every 6px `rounded-md` inside the modal region is corrected to `rounded-[3px]`: the three
  branding chips, `Create export`, `Close`, the download link (`ReceiptPanel.tsx`), and the preview's
  no-answer refusal box (`Preview.tsx`, the one `rounded-md` outside `ExportModal.tsx` that renders as
  this modal's `children`).
- **C1** -- every `font-weight: 500` (`font-medium`) in the same region is corrected to 400
  (`font-normal`) or 700 (`font-bold`): the two fieldset legends, the three chip states, `Create
  export`, `Close`, the download link, and `AppliedBranding`'s applied-label span (`font-medium` ->
  `font-bold`) -- one commit, cited to C1 and C8 together per the cell text.
- **Row S69** -- `ReceiptPanel.tsx` no longer synthesizes `state: 'LOADING'` for a null receipt.
  `submitting` (already tracked by `ExportButton`'s own `flow.submitting`, already used for the submit
  button's disabled state and label) is threaded into `ReceiptPanel`, which computes a LOCAL,
  three-value `receiptFlowState(receipt, submitting)`: `'receipt'` if a receipt exists, else
  `'submitting'` or `'idle'`. Rendered as `data-flow-state` on `[data-slot="receipt-panel"]`.
  `StatusPanel` (and so the literal string "Loading") mounts ONLY for `'receipt'`; idle/submitting show
  a plain placeholder line ("No export created yet." / "Creating your export...") instead. No change
  to the shared `EnvelopeState` enum -- the smallest correct surface, per the cell text's citation of
  the CTO's ruling.

## BEFORE / AFTER

- **C3 before**: `export/ExportModal.tsx:167` (pre-fix) `<Panel variant="chart">` -- the modal body
  rendered on the BAND (`#0A1733`), confirmed by this worktree's own pre-fix capture of
  `F71-AC10`'s invocation (not saved as a separate file; the fixed-state capture is
  `f71_chrome_1440.png`, whose `EXPECT-GROUND[[data-slot="branding-options"]]: PASS rgb(255, 255, 255)`
  line is the AFTER; the BEFORE state is textually established by `Panel.tsx`'s own
  `BACKGROUND_MAP.chart = 'bg-[hsl(var(--bg-band))]'`, i.e. `#0A1733`, never rgb(255,255,255)).
- **C3/C8 after**: `f71_chrome_1440.png`, `f71_chrome_390.png`, `f71_chrome_control.png` (the ground
  control, `--inject-css` repainting `branding-options` as `#0a1733`, correctly FAILS the ground
  assertion -- `ASSERT-GROUND: 0 of 1 met`). Read by eye: the modal body is a WHITE panel with a
  hairline, "Opal" is a navy-bordered bold-label chip (not filled purple), "Advisor"/"Co-branded" are
  muted grey (unavailable, no approved assets in this fixture), all text is navy/slate on white, no
  white-on-white legibility loss anywhere in the chrome.
- **Row S69 before**: `ReceiptPanel.tsx`'s (pre-fix) `envelopeFromReceipt`-or-`LOADING` branch meant a
  null receipt ALWAYS rendered `StatusPanel` with `state: 'LOADING'` (label "Loading"), whether or not
  a submit was in flight -- textually established by the removed lines
  (`{ state: 'LOADING' as const, sourceAsOf: null, safeActions: [], publicReasonCode: null }`).
- **Row S69 after**: `f71_idle_1440.png` ("No export created yet.", `Create export` enabled),
  `f71_submitting_1440.png` ("Creating your export...", `Creating export...` DISABLED button),
  `f71_received_1440.png` (a real `StatusPanel` card reading "Ready", `Download` link) -- three
  genuinely distinct markups, confirmed by `F71-AC14`'s bun:test guard (`receipt-flow-state.test.ts`,
  part (d): `idleHtml !== submittingHtml`, byte lengths 174 vs 181) and by the browser captures'
  `data-flow-state` attribute (`idle` / `submitting` / `receipt`).

## PER-CAPTURE RECORD

Every capture below ran with `--width` as stated, `--fixtures src/pages/InvestorReporting/__tests__/
fe-s-63/fixtures/export-ready.json` (three keys: `resolve-scope`, `performance-report`,
`holdings-snapshot`) unless it names `fe-s-71/fixtures/export-flow.json` (the same three keys plus
the authored fourth, `/api/scoped/investor-reporting/export`, for `submit-export`). DESIGN.md clauses
read against: C1 (typography weights), C3 (surface roles), C5 (inversion rule), C8 (accent/one
primary action), C9 (contrast), C11 (radius/elevation/focus).

| file | viewport | FIXTURES-MATCH | EXPECT*/ASSERT-* (verbatim) | clauses | verdict |
|---|---|---|---|---|---|
| f71_idle_1440.png | 1440 | matched 3 of 3 | `EXPECT[[data-slot="receipt-panel"][data-flow-state="idle"]]: PASS (1 visible)` / `EXPECT[[data-slot="submit-export"]:not([disabled])]: PASS (1 visible)` / `EXPECT-TEXT[[data-slot="submit-export"]::Create export]: PASS` / `EXPECT-STYLE[[data-slot="submit-export"]::border-radius]: PASS 3px` / `EXPECT-STYLE[[data-slot="submit-export"]::font-weight]: PASS 700` / `EXPECT-GROUND[[data-slot="export-modal"] [role="dialog"]]: FAIL null` / `ASSERT-CONTENT: 3 of 3 met` / `ASSERT-STYLE: 2 of 2 met` / `ASSERT-GROUND: 0 of 1 met` | C3, C5, C8, C11 | **F71-AC2 FAIL** (ground selector defect, row IRPT_FNTEND-W21-S1 -- content+style halves both hold) |
| f71_idle_390.png | 390 | matched 3 of 3 | `EXPECT[...idle]: PASS (1 visible)` / `EXPECT-GROUND[...]: FAIL null` / `ASSERT-CONTENT: 1 of 1 met` / `ASSERT-GROUND: 0 of 1 met` | C3 | **F71-AC3 FAIL** (same defect) |
| f71_idle_control.png | 1440 | matched 3 of 3 | `EXPECT[[data-slot="submit-export"]]: FAIL (0 visible)` (no `--click Export`) / `ASSERT-CONTENT: 0 of 1 met` (ground line not graded by this criterion's `<expect>`) | -- | **F71-AC4 PASS** |
| f71_ground_control.png | 1440 | matched 3 of 3 | `INJECT-CSS: ...` / `EXPECT-GROUND[...]: FAIL null` / `ASSERT-GROUND: 0 of 1 met` | -- | **F71-AC5 PASS-by-literal-match, VACUOUS** (row IRPT_FNTEND-W21-S1: the selector matches nothing before OR after the paint, so this control cannot discriminate the wrong-ground state it claims to test) |
| f71_submitting_1440.png | 1440 | matched 3 of 4 (4th key `DELAYED` but not yet fulfilled at capture time -- see note) | `DELAYED: api/scoped/investor-reporting/export (4000ms)` / `EXPECT[...submitting]: PASS (1 visible)` / `EXPECT[[data-slot="submit-export"][disabled]]: PASS (1 visible)` / `EXPECT-TEXT[...::Creating export...]: PASS` / `ASSERT-CONTENT: 3 of 3 met` | C3, C8 | **F71-AC6 PASS** |
| f71_submitting_control.png | 1440 | matched 3 of 3 | `EXPECT[...submitting]: FAIL (0 visible)` / `EXPECT[...disabled]: FAIL (0 visible)` / `ASSERT-CONTENT: 0 of 2 met` | -- | **F71-AC7 PASS** |
| f71_received_1440.png | 1440 | matched 4 of 4 | `EXPECT[...receipt"][data-job-state="ready"]]: PASS (1 visible)` / `EXPECT[[data-slot="download-link"]]: PASS (1 visible)` / `EXPECT-TEXT[...::Download]: PASS` / `ASSERT-CONTENT: 3 of 3 met` | C3, C8 | **F71-AC8 PASS** |
| f71_received_control.png | 1440 | matched 3 of 3 | `EXPECT[[data-slot="download-link"]]: FAIL (0 visible)` / `ASSERT-CONTENT: 0 of 1 met` | -- | **F71-AC9 PASS** |
| f71_chrome_1440.png | 1440 | matched 3 of 3 | `EXPECT-STYLE[...aria-pressed="true"]::border-radius]: PASS 3px` / `EXPECT-STYLE[[data-slot="submit-export"]::border-radius]: PASS 3px` / `EXPECT-STYLE[...close"]::background-color]: PASS null` (!= primary, holds) / `EXPECT-GROUND[[data-slot="branding-options"]]: PASS rgb(255, 255, 255)` / `ASSERT-STYLE: 3 of 3 met` / `ASSERT-GROUND: 1 of 1 met` | C3, C5, C8, C11 | **F71-AC10 FAIL** (both assertion families hold; the `<expect>` regex orders GROUND before STYLE, the instrument's fixed print order is CONTENT/STYLE/GROUND -- row IRPT_FNTEND-W21-S1) |
| f71_chrome_390.png | 390 | matched 3 of 3 | `EXPECT-GROUND[[data-slot="branding-options"]]: PASS rgb(255, 255, 255)` / `ASSERT-GROUND: 1 of 1 met` | C3 | **F71-AC11 PASS** |
| f71_chrome_control.png | 1440 | matched 3 of 3 | `INJECT-CSS: ...#0a1733...` / `EXPECT-GROUND[...]: FAIL rgb(10, 23, 51)` / `ASSERT-GROUND: 0 of 1 met` | -- | **F71-AC12 PASS** (genuine control -- the actual computed value changed) |
| f71_preview_scroll.png | 390 | matched 3 of 3 | `EXPECT[[data-slot="preview-scroll"]]: PASS (1 visible)` / `ASSERT-CONTENT: 1 of 1 met` | -- | **F71-AC13 PASS**; own probe (`portal/.scratch/probe-scroll.mjs`, not committed) measured `scrollWidth=1056`, `clientWidth=264`, `overflowX=auto` -- matches the cell text's own research numbers exactly; a genuine horizontal-scroll affordance, not permanent clipping |

**AC6's WIRE MATCH note**: `FIXTURES-MATCH: matched 3 of 4` with `FIXTURE-DEAD: /api/scoped/investor-
reporting/export` is the EXPECTED shape for an in-flight capture, not a defect -- `--clickwait 1200` is
shorter than the `4000ms` hold, so the route handler is still awaiting the delay (and has not yet
reached the `matchFixture`/fulfill branch that records a hit) at the moment the script reads its
assertions. `f71_received_1440.png` (no artificial delay, `--clickwait 3000` > the real resolve time)
shows the same fourth key cleanly matched, `4 of 4`.

## THE TWO TASK-ORDER DEFECTS (filed as IRPT_FNTEND-W21-S1)

1. **F71-AC2/AC3/AC4/AC5's `--expect-ground` selector**, `[data-slot="export-modal"] [role="dialog"]`,
   can never match in the live browser. Headless UI (`@headlessui/react` 2.2.9, driving
   `portal/src/ui/components/catalyst/dialog.tsx`, out of this cell's `<paths>`) portals the WHOLE
   `<Dialog>` subtree to a `#headlessui-portal-root` div appended at the END of `document.body` --
   `[data-slot="export-modal"]` (which sits OUTSIDE `<Dialog>` by FE-s-16's own design, precisely so
   its presence could answer "is the modal mounted" under SSR) stays in place, empty, once the dialog
   opens client-side, and `[role="dialog"]` lands in a completely different DOM subtree with no
   ancestor relationship to it. Measured directly with a standalone probe
   (`portal/.scratch/probe-dialog.mjs`, not committed): `document.querySelector('[data-slot="export-
   modal"] [role="dialog"]')` -> `null`; `[role="dialog"]` alone resolves to ONE element whose ancestor
   chain is `DIV#headlessui-dialog-_r_8_ < DIV < DIV < DIV#headlessui-portal-root < BODY < HTML`.
   Dropping the ancestor prefix, `--expect-ground '[role="dialog"]=rgb(244, 246, 250)'` PASSES exactly
   as AC2/AC3 need. **AC2 and AC3 are reported FAIL against their literal `<expect>`**, per BOUNDS'
   REFUSE clause -- the expectation is not edited. **AC4 PASSES** (its own `<expect>` never reads the
   ASSERT-GROUND line). **AC5 PASSES BY LITERAL MATCH BUT IS VACUOUS**: the same "matches nothing" FAIL
   occurs identically whether or not `--inject-css` painted anything, so the control cannot actually
   discriminate the wrong-ground state it is meant to test.
2. **F71-AC10's `<expect>` regex** requires `ASSERT-GROUND: 1 of 1 met` to appear BEFORE
   `ASSERT-STYLE: 3 of 3 met` in the output, but `scripts/ui-smoke.mjs` (frozen, out of this cell's
   grant) always prints assertion summaries in the FIXED order CONTENT, then STYLE, then GROUND. Both
   assertion families genuinely hold (`ASSERT-STYLE: 3 of 3 met`, `ASSERT-GROUND: 1 of 1 met`), but in
   the order STYLE-then-GROUND, so the `<expect>` pattern (which requires the reverse) never matches.
   **AC10 is reported FAIL against its literal `<expect>`.**

Full detail, evidence and vintages: surprise row `IRPT_FNTEND-W21-S1`,
`org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md`.

## NON-BROWSER GUARD (F71-AC14)

`receipt-flow-state.test.ts` (this cell's own `__tests__/fe-s-71/`), modelled exactly on
`__tests__/fe-s-9/receipt.test.ts`'s `renderToStaticMarkup` pattern: (a) no receipt, not submitting ->
`data-flow-state="idle"`, markup never contains "Loading"; (b) no receipt, submitting=true ->
`data-flow-state="submitting"`, still no "Loading"; (c) a ready receipt (`fixtures/fe-s-9/
receipt.ready.json`) -> `data-flow-state="receipt"`, unchanged download-link behaviour; (d) idle and
submitting markup are BYTE-DIFFERENT (174 vs 181 bytes), not merely prose-different. `bun test`: 4
pass, 0 fail, 12 `expect()` calls.

## PINNING SUITES (F71-AC15) AND WHOLE SUITE (F71-AC16)

`fe-s-9`, `fe-s-15`, `fe-s-16`, `fe-s-31`: 50 pass, 2 skip (browser precondition-absent on an
unrelated worktree port, not a code defect), 0 fail. `__tests__/fe-s-16/mounted-states.test.ts:146`'s
one literal-string assertion is updated in the SAME commit as the source fix, from
`<Panel variant="chart">` to `<Panel variant="nested">` -- the test's own comment states its intent is
"the two round-1 components are mounted INSIDE the ... Panel", never a specific variant, so changing
the variant is the correct fix, not a break routed around.

Whole `src/pages/InvestorReporting` suite: 623 pass, 22 skip, 0 fail, 2615 `expect()` calls, 645 tests
across 117 files. Dev server (port 5963) stopped and verified closed (`curl` returns `000`);
`IRPT_FE_DEV_PORT` unset in the shell that ran this suite.

**One self-inflicted regression found and fixed within this cell's own grant, before the final green
run**: this worker's OWN header-comment prose in `ExportModal.tsx` used backticks around the literal
text `text-white`/`border-white/N` (plain English, describing the fix) -- `__tests__/fe-s-11/
colour-law.test.ts`'s scanner treats ANY backtick-delimited string in the file as a template-literal
class token, so the comment's own code-formatting was flagged as a "light-on-canvas" violation at
`ExportModal.tsx:38` and, incidentally, broke that suite's own positive control (which asserted
`ExportModal.tsx` specifically DOES carry a flagged `text-white`, because before this fix it legitimately
did, inside `<Panel variant="chart">`). Fixed by removing the backticks from the comment (no code
behaviour changed); confirmed by a clean re-run of `fe-s-11/colour-law.test.ts` (4 pass, 0 fail) and the
whole-suite re-run above. Not filed as a surprise row: it was this worker's OWN authoring mistake in its
OWN write surface, caught and corrected before any capture or commit, never landing red.

## JUDGMENT (F71-AC17) -- RECORD, NO VERDICT

- `<Panel variant="nested">` is confirmed an EXISTING variant, not new: `Panel.tsx`'s own
  `PanelVariant` type already names `'chart' | 'nested' | 'mixed' | 'heatmap'`, and its decision-tree
  comment already names `nested`'s rule ("Visible nested containers -> SURFACE (--bg-surface,
  #FFFFFF) + hairline. DARK text only") before this cell touched the file.
- Every `text-white`/`border-white/N` class inside the changed region (`ExportModal.tsx`'s Branding
  legend, three chips, `no-approved-assets`, narrative-toggle + its unavailable span, account-detail
  label, optional-sections legend + item labels; `AppliedBranding.tsx`'s applied-label weight;
  `ReceiptPanel.tsx`'s download link) is flipped to a navy/slate equivalent -- captured before (textual,
  via `Panel.tsx`'s BACKGROUND_MAP and the removed source lines, since no BEFORE screenshot of this
  exact cell's own regression was taken separately from the AFTER) and after (`f71_chrome_1440.png`,
  `f71_chrome_390.png`, `f71_idle_1440.png`, `f71_submitting_1440.png`, `f71_received_1440.png`).
- `S69`'s three states (idle, submitting, receipt) are read as genuinely distinct MARKUP, not merely
  distinct prose: `F71-AC14` part (d) diffs the raw HTML bytes (174 vs 181), and the browser captures
  carry three distinct `data-flow-state` values plus three visually distinct card renders (a plain
  placeholder line for idle/submitting, a real `StatusPanel` "Ready" card with a `Download` link for
  receipt).
- The preview's horizontal scroll is confirmed REACHABLE, not merely captured: the probe measured
  `scrollWidth=1056` vs `clientWidth=264` (`overflowX: auto`) at 390px, matching the cell text's own
  cited research numbers, so the content genuinely overflows its container by more than 4x and the
  `overflow-x-auto` container is exercisable, not decorative.
