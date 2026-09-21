# IRPT_FNTEND.TO-FE-s-63 -- closing pass, export modal and print page -- result

**These captures are FIXTURE-FED and, for the ordered invocations, NOT EVEN THAT.** They are the real route with responses answered at the network layer by `ui-smoke.mjs`; no live route was reached. That is the right kind of evidence for FWD-12's DONE WHEN (familiarity of the real page against DESIGN.md), which needs no counterpart half, unlike the other seven cards. BUT the fixtures the order names do not construct the state: every ordered capture printed FIXTURE-DEAD (`FIXTURES: 5 declared; 0 matched` for the modal, `3 declared; 0 matched` for print), because the fixtures key on route names the v1 client no longer requests. Row `IRPT_FNTEND-W13-S1`. So the export modal below is its EMPTY/no-report state, and the print route rendered only its refusal panel: NO print document rendered in this pass.

## Captures (all in this folder)

| file | viewport | CANVAS line, verbatim | what I saw |
|---|---|---|---|
| fe-s-63_export_1440.png | 1440 | `CANVAS: rgb(244, 246, 250)` | modal open over a blurred page; fixtures dead. |
| fe-s-63_export_390.png | 390 | `CANVAS: rgb(244, 246, 250)` | same modal, full-width sheet. |
| fe-s-63_print_1440.png | 1440 | `CANVAS: rgb(244, 246, 250)` | "This bundle was not rendered ... perf-narrative-fixture-1 is absent" on a SILVER ground. |
| fe-s-63_print_390.png | 390 | `CANVAS: rgb(244, 246, 250)` | same refusal (390 px). |
| fe-s-63_diag_export_ready_1440.png / _390.png | 1440/390 | `CANVAS: rgb(244, 246, 250)` | fe-s-16-ready.json: 2 of 3 fixture keys matched; modal unchanged (no performanceReport). |
| fe-s-63_diag_print_narrative_1440.png / _390.png | 1440/390 | `CANVAS: rgb(244, 246, 250)` | working-shape URL from F18-AC12; still refused ("rev-49f-000091 is absent"). |
| fe-s-63_fix1_before / after_print_ground_1440.png | 1440 | `CANVAS: rgb(244, 246, 250)` both | before silver, after light. |

Discriminator: FE-s-11's recorded capture printed `CANVAS: rgb(195, 202, 218)` (the retired silver). Mine print `rgb(244, 246, 250)` on every run, and the print PNG is nonetheless SILVER (about rgb(196, 203, 219) by eye). So the CANVAS line has an arm that can fail for the app body but does not measure `.ir-print-root`: a green CANVAS beside a silver print ground (row W13-S2).

## Findings, by DESIGN.md clause (read in the PNGs unless marked SOURCE)

- **C3 (print ground)**: print route ground silver #c4cbdb (print.css:139). FIXED, see below.
- **C3 (dark panel)**: the export modal body is a navy `Panel variant="chart"` (#0A1733-family fill) inside a white dialog, with a white inner card and a white preview card inside it: a dark container that is not the one band, and a panel inside a panel (SOURCE ExportModal.tsx:167; header says it is held by a colour-law test anchor). NOT fixed: the fix is a redesign of the modal and its colour-law test.
- **C9 / C5.8 (contrast)**: the modal's "Every field ... not known" line is dark red on navy, essentially unreadable in the 1440 and 390 PNGs; source uses `text-white/70` and `/50` idioms (ExportModal.tsx:199,213) which C5.8 forbids. NOT fixed.
- **C8 (accent)**: purple fills on the "Opal" branding chip AND the Close button in one view (two purple fills; C8 says a segmented control never gets a filled purple chip per option). NOT fixed.
- **C11 (shape)**: the dialog sheet corner radius reads about 12 px at 1440 and 390 (C11 allows 2/3/4 px); the dialog comes from the catalyst `Dialog`, not `export/`. Not mine to fix.
- **C11 / C1 / C2 (SOURCE only, not capture-demonstrated)**: print.css:520 `box-shadow` on `.ir-page`, print.css:290 `.ir-mono` in Consolas.
- **PRD constraint "modals, previews and exports carry the same brand as screens"**: the print ground before the fix did not (silver vs the screens' #F4F6FA); after the fix the screen ground does.

## Fix made (one)

Finding: print route screen ground silver #c4cbdb, DESIGN.md C3. BEFORE `fe-s-63_fix1_before_print_ground_1440.png`; AFTER `fe-s-63_fix1_after_print_ground_1440.png` (light canvas). Change: `render/print.css` `.ir-print-root { background: #f4f6fa }` (screen plane; `@media print` already white). The whole IRPT_FNTEND suite stayed green afterwards (612 pass, 22 skip, 0 fail). Portal commit f074ed3f (LOCAL).

## F60-AC6 color-law question (part 2 of F63-AC8)

NOT rendered. No print document rendered at portal HEAD, so the partial-disclosure note's on-screen appearance was NOT READ (row W13-S3). SOURCE only: `.ir-note` (print.css:272-276) and `.ir-muted` (:285-287) are #595959 and sit on the white `.ir-page` sheet. DESIGN.md's C3 surface roles are page, panel, band, sunken; no clause names a print sheet, and #595959 is in no C3/C9 ink table (C9 secondary is #6B7280 on a panel). So, as a finding: no DESIGN.md clause speaks to a print sheet as such.

## Criteria

F63-AC1 rc=0. F63-AC2 `CLICKED: Export`. F63-AC3 and AC4 the CANVAS line matched, on a fixture-less state. F63-AC5 and AC6 REFUSED: no `REFS RESOLVED` line (row W13-S1). F63-AC7 `0 fail` with the server stopped and port 5483 verified closed (curl 000). F63-AC8 recorded, no verdict.
