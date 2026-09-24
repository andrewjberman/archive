# FE-s-63 result, second pass (replacement instance of 0.9.0_WK_IRPT_FNTEND~13)

**FIXTURE-FED, not a live route.** Every capture below is the real `investor-reporting` route (and the real `investor-reporting/print` route) served by this worktree's own dev server on port 5494, with the network answered by two fixtures I authored (`__tests__/fe-s-63/fixtures/export-ready.json`, `print-ready.json`); no live backend was reached. That is the right evidence for THIS card and not for the other seven: FWD-12's DONE WHEN is about how the page LOOKS and behaves to an advisor who already uses the portal, which is a property of the front end's rendering of a READY payload, and it has no backend counterpart half (IRPT_BCKEND is not engaged). A fixture at the network layer holds the state constant so the reading is of the page, not of the data.

First-pass evidence (fixtures that matched no request; a print route that never rendered) is kept under `pass1/`. The portal print-ground fix (`.ir-print-root` #c4cbdb to #f4f6fa, DESIGN.md C3) was made and drained in pass 1 (portal 8894e765); its BEFORE/AFTER PNGs are in this folder.

## Runs (all quoted from the run outputs, ANSI stripped)

| Criterion | Deciding lines |
|---|---|
| F63-AC2 / AC3 (export 1440) | `CLICKED: Export`; `CANVAS: rgb(244, 246, 250) (the page field; contract portal/DESIGN.md C3 = #F4F6FA ...)`; `FIXTURES: 3 declared; 3 matched >=1 URL` |
| F63-AC4 (export 390) | `CLICKED: Export`; `CANVAS: rgb(244, 246, 250) (...)`; `FIXTURES: 3 declared; 3 matched >=1 URL` |
| F63-AC5 (print 1440) | `CONSOLE[log]: REFS RESOLVED: 1 of 1` (printed twice); `CANVAS: rgb(244, 246, 250) (...)`; `FIXTURES: 2 declared; 2 matched >=1 URL` |
| F63-AC6 (print 390) | `CONSOLE[log]: REFS RESOLVED: 1 of 1` (printed twice); `CANVAS: rgb(244, 246, 250) (...)`; `FIXTURES: 2 declared; 2 matched >=1 URL` |
| F63-AC1 | `tsc -b --noEmit`, rc=0 |
| F63-AC7 | 612 pass, 22 skip, 0 fail, 634 tests across 114 files, rc=0; dev server stopped first (listener 28084 stopped, curl 000, Get-NetTCPConnection count 0) |

No `FIXTURE-DEAD` line in any run. Discriminator: FE-s-11's recorded silver capture printed `CANVAS: rgb(195, 202, 218)`; these print `rgb(244, 246, 250)`. Caveat (row W13-S2): the CANVAS line reads the page field, not the modal or print ground, so it cannot see those; the PNGs were read for that.

## Item 2: which step rejected "rev-49f-000091 is absent"

`export/resolveBundle.ts:224-227`, in `resolveOne`: when the cache has no entry for (op, revision) and the fetcher throws, it raises `MissingPayloadError(String(op), revision)`, whose message (`render/manifest.ts:296`) reads "... cannot render reportKind '<op>': <revision> is absent" and is shown by `render/PrintEntry.tsx:191` as "This bundle was not rendered". The fetcher throws when the request it issues gets no usable answer. **Classification: FIXTURE defect, not a print-path defect.** The first-pass fixtures were keyed to retired operation names, so the wire requests matched no key (0 of 3 matched in pass 1); with the keys repaired (`/api/scoped/investor-reporting/performance/`, `/narrative/`) the same route renders. No file under `export/` or `render/` was changed in this pass. Limit: I did not re-run the original `fe-s-16-print-narrative.json` from this pass; the inference rests on the source reading plus the pass-1 0-of-N match counts and the pass-2 2-of-2 match. The `.scratch/mut_*.json` mutants left by the previous instance each differ from print-ready.json in several fields at once (fewer summary rows, shorter series, a different calculation_id, missing status and unprojected_grant); they were not single-field mutants and I draw no conclusion from them beyond that.

## Captures: what was seen (files in this folder)

- `fe-s-63_export_1440.png`, 1440 wide. CANVAS as above. Clauses: C3 (page field #F4F6FA behind a dimmed overlay; white dialog; navy panel inside it), C8 (purple selected chips and Create export button), C11 (dialog radius). Saw: a white dialog titled Export holding a navy "EXPORT OPTIONS" panel with Branding chips (Opal selected, Advisor, Co-branded), a "period in context" checkbox (unchecked), "Account detail" (checked), a white "Branding applied: Opal" card whose status row reads "Loading / No source age yet", a Create export button, and below it an Opal-branded rendered preview of the report (logo, "Report state: Ready | Business date 2026-09-09", 2026-01-02 to 2026-09-09, UNAVAILABLE beginning/ending values) cropped at the right by the panel. The status row in the card says Loading although the preview beneath it is READY: I could not confirm from this fixture that the card's own state is READY, and I did not investigate further (time-box); recorded as an observation, not a finding.
- `fe-s-63_export_390.png`, 390 wide. Same content in one column; the preview is clipped at the right edge of the panel; the dialog runs off the bottom of the 900 px capture. Same clauses.
- `fe-s-63_print_1440.png`, 1440 wide. Four A4-style white pages on the #F4F6FA ground (C3): 1 performance report with return chart and table, 2 "The period in context" with chart and two event markers (trough 2026-04-07, recovery 2026-06-19), 3 period results and account table, 4 methods and sources. Opal logo and navy/purple headings on each page. Saw a real document, not "This bundle was not rendered".
- `fe-s-63_print_390.png`, 390 requested; the document lays out at 1056 px (the sheet does not reflow to the phone width; it scales down in the capture). Same four pages.
- `fe-s-63_print_1440_period_note_crop.png`: crop of page 2 head.

## Item 3: F60-AC6, the period-in-context partial-disclosure note, RENDERED and READ

Producing it needed no change to print-ready.json: the fixture's narrative response carries `unprojected_grant` (count and denominator) at envelope level, which `PeriodInContextPage.tsx:100-110` reads from `packet.availability.unprojectedGrant`. Rendered, page 2, directly under the fixed statement: "1 of 5 events not yet reflected in this narrative." It appears as one line of small light-weight grey text (`ir-note ir-muted`, #595959 per `render/print.css:272-287`) on the white page sheet, the same grey as the fixed statement above it and visibly quieter than the navy headings; it reads as secondary text, legible on white. Which DESIGN.md clause speaks to a print surface: **none that I found.** C3 names page canvas, panel, band and sunken; C9's secondary ink is stated for a panel; #595959 appears in no C3 or C9 table (print.css's own header names navy #0A1733 and charcoal #595959 as its two inks). This is a finding about a gap in the contract, not a conformance or non-conformance. F63-AC8 is judgment: evidence above, NO verdict; recorded UNVERIFIABLE-BY-INSTRUMENT.
