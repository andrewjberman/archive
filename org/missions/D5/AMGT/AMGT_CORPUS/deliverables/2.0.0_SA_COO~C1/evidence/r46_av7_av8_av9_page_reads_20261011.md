# AMGT_CORPUS round 46 -- CRPS-av-7, av-8, av-9: the page reads for FWD-15, FWD-16 and FWD-21

**Issuer:** `2.0.0_SA_COO~C1` (dell1), 2026-10-11 12:47Z-13:05Z. **Instrument:** `/ui-walk` (`walk.mjs --route /security-analysis --security
"UNVGY US" --security "ADBE US"`) on the local `dev:live` build (this seat started it on 5174; the earlier server on that port was another
seat's and had stopped), plus the live-payload reads in `checks/round46/` (`av_capture.py`, `av7_posture_reads.py`, `av9_forecast_reads.cjs`).
The portal working copy under the walk is `DEV` `8ed372cb`; it does not carry av-2. The walker armed at 12:48Z and disarmed at 12:51Z (a login
afterwards: 401, REFUSED); an earlier attempt at 12:47Z found port 5174 down, armed and disarmed cleanly and read nothing. A walk is a
development instrument and grades nothing; the CVO grades. Screenshots and `findings.json` stay local (`tmp/ui-walk/20261011T124808Z/`,
gitignored); this record states what was read in words. Live function: `SOzAz9/gfKE++UOSB8qWSDJvhOsDQMoE+DDPzaFbeSI=` (09:26:42Z).

## FWD-15 -- av-7 (PRD:485-487): "both render cited on the header posture line and the Posture tab, and the machine verdict is byte-unchanged"

| clause | read |
|---|---|
| the Posture tab renders both, cited | IMB LN's Posture tab (round-45 walk, screenshot 031) reads "Fund of record: IDVZ; last stated position: Potential ADD in IDVZ (currently ~2.5%)" with "Source: Imperial Brands Research Pack 2026 07 17_v1". `PostureTab.tsx:585-586` is the only non-harness reader of `fund_of_record` and `last_stated_position`. Live payloads: a cited fund of record on **40 of 95** names, a cited last stated position on **47 of 95** (`evidence/r46_av7_posture_reads_20261011.txt`). |
| the header posture line | **NOT PRESENT on the page as built.** The first screen's header (IMB LN, UNVGY, ADBE read) carries identity, the figures strip, Chatter and Breakout, and no posture line. `DossierPositionLine` is not defined anywhere in `portal/src` outside harness comments; `PostureHeaderLine` is exported from `components/LeadPanel.tsx:316` and is "unused by this file's own render" (LeadPanel.tsx:83). The removal rode DSGN_AMGTV1 AV-zzk-3 (`29eb8ed4`, 2026-10-09, "tabs in the first screen, identity once, plumbing out of the face"). The round-40 harness arm (`page_check.cjs ap3`) no longer loads: `DossierPositionLine is not a function in module scope`. |
| the machine verdict is byte-unchanged by their presence | the served `posture.verdict` and `as_of` equal the STORED posture object (`posture/v1/<key>/<as_of>.json`) on **33 of 33** names that have one; the other **62** have no stored object and serve a block that is not SERVED (absent both). The verdict is the machine's, read beside the cited lines, not computed from them. Limit: the stored object is read through `scoped_amgt.read_pool_object`, the function the API uses, not by a second reader. |

So FWD-15's Posture-tab half is read and the verdict clause holds; the header-line half names a surface a later design cell removed. Row
`AMGT_CORPUS-D1-S4` carries it; whether the outcome's wording is amended or the line restored is the CTO's.

## FWD-16 -- av-8 (PRD:521-523): a PDF-only name rendered end to end -- ADBE US

ADBE US is shape pdf in the FWD-16 census (pillars 2, management 1, cases 3 on both /10 and /11). On the page:

- **Pillars (Thesis tab):** 2 pillars, each a lead line then its paragraph under "The research team's thesis pillars", each with "Source: ADBE research pack 7_13_2026" and a "Where this comes from" opener (the pillar text is the team's: "Expanding market opportunity..."; "Entrenched standard for creative professionals..."). The openers were not pressed in this walk.
- **Management (Exec Management tab):** "The research team on management" carries the team's passage (CEO and the two internal frontrunners, capital allocation) with its source line, and a MACHINE officer table of 7 officers (Chair/CEO through VP:Investor Relations).
- **Cases (Model tab):** "The research team's base case", "upside case" and "downside case", each five columns 2026E-2030E with EPS, Multiple, Price, Return, "Source: the research team's pack, ADBE research pack 7_13_2026".
- ADBE's own rows are `master_absent` (the model template is not in the stored library); the tab says so in one line above "All figures".

The docx control is not rendered in this walk (it is the census's: pillars KEPT 10, none LOST).

## FWD-21 -- av-9 (PRD:615-618)

| clause | read |
|---|---|
| names whose block carries forecast years render 2026E-2028E beside the history | **94 of 94** names with served forecast figures render E year columns (`av9_forecast_reads.cjs`, the real `buildModelSheet`); ADBE US's Key figures read 2026E and 2027E beside 2025 on the page |
| the history columns are byte-unchanged | the history year columns of every row of every group are JSON-equal between the build with the served forecasts and the history-only build on **95 of 95** names |
| a name without forecasts reads the reason | one name, UNVGY US: `forecast_figures` 0, served `forecast_reason` "no forecast figure is served: no BEST_PERIOD_END_DATE for this period (FY1, FY2, FY3)". ON THE PAGE (Model tab, "All figures" fold footnote, in words): "2026E, 2027E, 2028E: no consensus estimates are served for this name; the model block carries fiscal years 2015 to 2025." Key figures show the 2025 column only. The old wrong sentence ("pulled before C-MODEL-FORECASTS", round 41) is gone. The served string names a vendor field; the page does not show it. |

17 non-December fiscal-year names showing 2027-2029 is the CTO's "CORRECT, not a defect" (round-45 analysis) and is not re-read here.

## Other walker findings on these two names (none grades an outcome)

Control `Earlier month` not found; truncated labels; no timeline day bar; no timeline event element on either name; two date formats; two
money formats; 2 console errors (not read here).
