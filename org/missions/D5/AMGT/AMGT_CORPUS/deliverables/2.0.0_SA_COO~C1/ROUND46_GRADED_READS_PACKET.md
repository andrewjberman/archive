# AMGT_CORPUS round 46 -- CRPS-av-11: the graded-read packet for FWD-11, 15, 16, 21 (and, once av-10 is read, FWD-12 and FWD-20) for `3.0.0_SA_CVO`, L9

**Issuer:** `2.0.0_SA_COO~C1` (dell1). **Source:** `ledger/ROUND_ANALYSIS.round45.md` @0d399ece09 s.2 items 2-5. Status: **PARTIAL.** FWD-11, 15, 16 and
21 are read (below). FWD-12 and FWD-20 wait on av-1 and av-2 draining, the /12 write (av-3), the API redeploy (av-4) and the portal DEV landing
(av-5); the rendered re-read (av-10) grades them. Paths are relative to `org/missions/D5/AMGT/AMGT_CORPUS/`; `C1/` = `deliverables/2.0.0_SA_COO~C1/`.
All page reads below were taken on live function `opal-amgt-scoped-api` `SOzAz9/gfKE++UOSB8qWSDJvhOsDQMoE+DDPzaFbeSI=` (09:26:42Z, the AMGT_RESAPP
qq-5 redeploy), with the shared portal working copy DEV `8ed372cb` (it does not carry av-2).

| outcome | read | evidence | read says |
|---|---|---|---|
| FWD-11 | av-6, on the LIVE function | `C1/evidence/r46_av6_roster_compare_live_20261011.txt` | SAP GY served 6 = filing 6, same names 6, same roles 6, in text 6; BABA US served 7 = filing 7, 7, 7, 7 (order differs: printed, not graded). `av6 unchanged 2/2`. Round 45's read of the same comparison ran through the local module (`r45_au5`); this one reads the live `/thesis` payload's `management` block. |
| FWD-15 | av-7 | `C1/evidence/r46_av7_av8_av9_page_reads_20261011.md`, `C1/evidence/r46_av7_posture_reads_20261011.txt` | Posture tab renders both cited (cited fund of record 40 of 95 names, cited last stated position 47 of 95); verdict equals the stored machine verdict on 33 of 33 names that have one (62 have none). **The header posture line is not on the page as built** (removed by DSGN_AMGTV1 AV-zzk-3 `29eb8ed4`); row `AMGT_CORPUS-D1-S4`, the outcome's wording is the CTO's. |
| FWD-16 | av-8, ADBE US (shape pdf) | the same md, section FWD-16 | 2 pillars with lead, paragraph, source and opener; management passage plus a 7-officer table; base, upside and downside cases 2026E-2030E from the team's pack. The docx control stays the census's (round-45 packet: pillars KEPT 10). |
| FWD-21 | av-9 | `C1/evidence/r46_av9_forecast_reads_20261011.txt` and the md | history columns JSON-equal with and without the forecasts on 95 of 95; 94 of 94 names with forecast figures render E columns; UNVGY US reads, in words in the "All figures" fold, "no consensus estimates are served for this name; the model block carries fiscal years 2015 to 2025" (the old wrong sentence is gone; the served string still names a vendor field and is not shown). |

## What each read does not say

- FWD-11: `read_management` and the filing parse are the code's own reads; "by content, name by name" is the comparison. The live function is
  the SERVED side; the filing roster is parsed by the local `roster` module.
- FWD-15: the verdict read is stored-versus-served through the API's own pool reader, not a second implementation.
- FWD-16: one PDF-only name was rendered (ADBE US); the openers were not pressed in this walk.
- FWD-21: the 17 non-December fiscal-year names showing 2027-2029 are the CTO's "CORRECT, not a defect".

## FWD-12 and FWD-20 -- av-10 (the rendered census)

**State at 14:05Z.** av-1 and av-2 are drained; av-2 is on portal DEV (`f00c7b8ee8`); the /12 write (av-3) is read Branch A (95 of 95, ledger closed
@444123834e); the API redeploy (av-4) is AMGT_RESAPP's `ff-4` window, earliest GO ~15:00Z. The LIVE function still serves /11, so the REAL read
(`av_capture.py` over the live function, then `av10_rendered_census.cjs`) is NOT taken yet and nothing below is graded on it.

**PRE-READ, a prediction, labelled as one.** `av10_preread_inject.py` puts each name's STORED /12 `team_sheet` (exactly what the API will return
once it picks the /12 objects) into the live capture; `av10_rendered_census.cjs` runs the REAL `modelSheet.ts` of DEV `f00c7b8e` over it
(`C1/evidence/r46_av10_preread_census_20261011.txt`):

| read | predicted result |
|---|---|
| classes over the 32 own workbooks | FIGURE 3381, HEADING 316, CONTROL 62, sum 3759 = the sheets' rows; per-name sums hold |
| FIGURE rows by source | Bloomberg 482, team's own value 2899, why 0, refused 0, **unmapped 0** (sum 3381) |
| rendered | 316 heading rows, 0 CONTROL rows rendered, 0 why-rows with a barred word |
| the first group | equals the sheet's non-CONTROL rows, in order and labels, on 32 of 32 names with team rows |
| names | 63 `master_absent` render the base rows with the served reason; the master template is still not in the library |

Of the 497 FIGURE rows whose label matches a row spec, 482 have a served Bloomberg figure and 15 fall to the team's value (precedence 1 needs a
served figure). The 4,296 text cells (for example `#VALUE!`) are not rendered as values by the builder's rule (a team cell is a finite number only; av2_check arms b4 and b5 pin it); this pre-read does not re-read those 4,296 cells one by one.
**Limit:** the sheet builder on stored fields, not a browser DOM walk and not the live payload; the post-act read replaces it.
