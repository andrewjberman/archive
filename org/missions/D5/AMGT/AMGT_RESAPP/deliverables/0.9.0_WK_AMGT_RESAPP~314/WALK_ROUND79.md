# WALK_ROUND79 -- AMGT-cc-8, worker 0.9.0_WK_AMGT_RESAPP~314

Records what was seen; no verdict on any act. The walker account is role admin, userType Dev: role-gated differences are NOT covered.
History: the first attempt stopped on contention (rows `AMGT_RESAPP-Z-W314-S1` and `-S2`, committed `d03508571e`, left as filed). The issuer's
RE-GO of 2026-10-08T21:51:49Z ordered the walk in full; this record is that walk.

## Build, instrument, safety

- Build walked: local dev build `http://localhost:5174`, started by this worker with `bun run dev:live --port 5174` from
  `C:/tmp/r79-308/portal` (port 5174 read 0 listeners and the walker read disarmed before arming; the listener afterwards was this
  worker's own, parent chain checked). Portal ref `38cc0ecf` (`git -C portal rev-parse --short HEAD`), branch `wk-AMGT_RESAPP-314-portal`. No bun install. Live function per the GO.
- PRD quotes at `prd_version` v0.41 (`org/missions/D5/AMGT/AMGT_RESAPP/prd/AMGT_RESAPP_PRD.md`).
- Walker slot: `status` read `status=disabled ... armed=no armedBy=none; SSM ABSENT` before each of three arms, and after the last. Each run was
  armed and disarmed by the walker; each ended `LOGIN WITH THE WALK PASSWORD AFTER DISARM: HTTP 401 ... REFUSED`:
  | pass | stamp (gitignored `tmp/ui-walk/`) | holder | disarmed | screenshots |
  |---|---|---|---|---|
  | 1 recon + raw reads (`instrument/cc8_recon.mjs`) | `20261008T220016Z` | `Opal_Bloomberg:24732:a3731300` | 22:02:44Z | 6 |
  | 2 walk (`instrument/cc8_walk.mjs`, first draft) | `20261008T220747Z` | `Opal_Bloomberg:12616:c200a579` | 22:09:38Z | 27 |
  | 3 walk, the pass recorded below (`cc8_walk.mjs` as committed) | `20261008T221220Z` | `Opal_Bloomberg:10252:fd812ac3` | 22:14:27Z | 29 |
  Pass 2 never listed Boeing among the ten rows (a name-match slip: `BA_US` is inside `BABA_US_Equity`), read the BA chart's y-axis
  ticks with a selector that found none, and made no figure press on ASML NA; pass 3 fixed the first, added the svg-text tick read and added the figure press. Everything below is pass 3 unless it says otherwise.
- Instrument: `instrument/walk_ay6.mjs` and `signin_detect.mjs` copied unchanged from round 78; modules `cc8_recon.mjs` and `cc8_walk.mjs` are this round's (extended from `bb19_walk.mjs`). GET only; the guard
  is unchanged: pass 3 0 guard aborts, 0 API issues, 2 console errors (the sign-in page's 401s), walk void: no. Third-party document requests are aborted in the browser context.
- Captures COPIED to `captures/`: 29 PNG from pass 3 (`001`-`029`), same file names as in the stamp. `data/run3/` is pass 3's data folder (`captures.json`, `fwd7/`, `fwd18/`, `fwd1/`, `sections/`, `api/`, `walk_stdout.log`).
- Positive control (`data/run3/captures.json`): 29 of 29 captures carry a route and 0 capture errors; 12 of 12 `/freshness` captures read `/freshness`; 17 of 17
  `/security-analysis/<key>` captures carry all five tab labels `Thesis, Exec Management, Peers, Model, Posture`; 29 of 29 PNG files are over 5 KB.
- What the page draws against what the SERVER sends is read from the dev build's own signed-in API client: `GET /api/scoped/amgt/security/<key>/thesis` and `GET /api/scoped/amgt/freshness?view=page`
  (status 200 for all five names and the freshness view), from inside the page with the headers the page itself sent. The portal source at this ref has one reference to `segment_table` (a type in `types.ts`) and none to `dossier_sections` or `seeking_alpha` outside test harness files.

## FWD-18

DONE WHEN (quoted, v0.41 lines 678-681): "EXERCISED -- (v0.40) a seat clicks, on demand, a filing-derived figure on a covered company the grading seat names, through to the passage it came from. An analyst's own click stays the ACCEPT".

### ASML NA (`ASML_NA_Equity`), Thesis tab

1. **The place where a driver chart would be** (capture 013; `data/run3/fwd18/ASML_chart_place.json`): a sentence in a bordered white panel, no chart (0 svg, 0 buttons, element `data-driver-chart="ABSENT"`),
   quoted: "The filing text kept here counts the company's own shares or describes its share capital, so no driver chart is shown." It sits directly under the panel "BUSINESS SEGMENTS -- FROM THE FILING", which reads "The filing text kept here is about the company's share capital and who holds its shares, so no segment breakdown is shown."
   API client (`data/run3/api/thesis_ASML_NA_Equity.json`): `thesis_driver_chart` status `ABSENT`, `refused` true, `points` 0, `driver_series` "Issued ordinary shares outstanding (nominal EUR0.09), reflecting the buyback authorization", `driver_unit` "number of shares", and the same `plain_reason` sentence: the page draws the served sentence.
2. **A figure in the thesis text that can be pressed.** On the Thesis tab the three cards read "Investment thesis is not in this pack yet. The research team fills it in.", "Risks is not in this pack yet. ..." and a Recommendation card ("The updated Dutch Corporate Governance Code 2025 applies to financial years starting on or after January 1, 2025, and..."). The tab itself holds no pressable figure
   (`data/run3/fwd18/ASML_thesis_panel_pressables.json`: the two "Where this comes from" summaries and the three card buttons; none on a figure). The card press opens a window.
   - THE ONE CARD PRESS: "Investment thesis" (capture 013 before, 016 after). The window (`role=dialog`) reads: "No company description is on file yet." then "FILED DETAIL (DOES NOT DESCRIBE THE BUSINESS)", then the drafted sentence "MACHINE Board holdings: members of ASML's current Board of Management and Supervisory Board (8 persons) held 51,095.11 shares, or 0.01%.", with two passages written out beneath it, inline, no control on them:
     - passage `P0064`: "Members of ASML's current Board of Management and Supervisory Board (8 persons) 3", citation line "ASML NA'S 20-F, FILED FEBRUARY 25TH, 2026 -- ITEM 3.D. RISK FACTORS > 5.09% > PARAGRAPH 65";
     - passage `P0065`: "1. Based solely on the Schedule 13-G/A filed by Blackrock, Inc. with the SEC on April 23, 2025, BlackRock, Inc reports voting power with respect", citation line "... -- ITEM 3.D. RISK FACTORS > 0.01% > PARAGRAPH 66"; footer "Source: machine draft from ASML NA's 20-F, filed February 25th, 2026".
   - THE ONE FIGURE PRESS: the figure "51,095.11" itself in that sentence (captures 017 before, 018 after; `data/run3/fwd18/ASML_figure_press.json`). The cursor over it reads `auto`. Nothing changed: dialogs 1 before and after, dialog text length 798 before and after, passages 2 before and after, URL unchanged, browser pages 1 before and after, no new popover. The figure is plain text, not a control; the passage the sentence rests on is already drawn under it once the card is open (so the passage, filing, heading and paragraph above are what is read, not what the figure press opened). The probe that reports its nearest interactive ancestor matched a container (read true; the element was not identified, and the cursor and the unchanged state are what is recorded).
   - The other two windows (captures 019 Risks: "Risks is not in this pack yet. The research team fills it in.", no passage; 020 Recommendation: the research team's base, upside and downside cases as tables of EPS, multiple, price and return for 2026E-2030E, then the machine-draft sentence with passage `P0002` "to the financial years starting on or after January 1, 2025," -- ... ITEM 3.D. RISK FACTORS > GOVERNANCE CODE 2025 WAS PUBLISHED, WHICH APPLIES > PARAGRAPH 3).
   - API client, same names: `thesis_driver_chart.points` 0; the served drafted sentence and passages are the ones drawn.

### BA (`BA_US_Equity`), Thesis tab

- The chart is drawn: caption "Commercial Airplanes (BCA) aircraft deliveries -- from the filing, not the model", three points 2023, 2024, 2025, a line with three dots, and the line "3 fiscal year(s) from the filing". Before the press, under the chart, three link buttons: "2023: 528 -- show the filing passage" (passage `P0278`), "2024: 348 -- ..." (`P0277`), "2025: 600 -- ..." (`P0276`), each `aria-expanded=false`. Capture 021.
- **y-axis tick labels** (read from the chart's svg text, `data/run3/fwd18/BA_chart_before.json`): `0`, `150`, `300`, `450`, `600` (no `K`/`M` suffix, none in the "393.4M" form); x ticks `2023`, `2024`, `2025`. (A class-based selector for the tick labels read none in passes 2 and 3; the svg-text read, added in pass 3, is the one recorded.)
- THE ONE PRESS: the 2025 point's link "2025: 600 -- show the filing passage" (the drawn dots carry no press handler of their own, so the point is pressed through its link). Capture 021 before, 022 and 023 after.
  - **Passage rendered once**: 1 passage block in the chart (`blockquote` count 1), and the passage's first 60 characters occur 1 time on the whole page (`occurrences_of_probe_on_page` 1). The link now reads `aria-expanded=true`.
  - What opened, drawn as a table: "2025" over columns 737, 747, 767, 777, 787, Total; row "Cumulative deliveries 9,240 1,573 1,351 1,776 1,249"; row "Deliveries 447 (7) 30 (15) 35 88 600"; the sentence "Some rows list a different number of figures than there are columns, because the filing's blank cells and footnote marks are not kept; those rows give their figures in the order printed and may not line up with the columns."; citation line "From the filing: ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / TABLE 2025". The passage block carries `data-driver-chart-passage-source="served"`. The segment panel above the chart reads "From the 10-K filed January 30th, 2026."; the chart's own passage line names an item and table, not the filing's date.
- API client (`data/run3/api/thesis_BA_US_Equity.json`): `thesis_driver_chart` served with 3 points, the same values 528, 348, 600.

## FWD-1

DONE WHEN (quoted, v0.41 lines 493-496): "EXERCISED -- (v0.40) a seat opens, on demand, a covered company the grading seat names, and the model numbers, the business description and the segment breakdown are on screen with no spreadsheet or data terminal opened. An analyst's own use stays the ACCEPT".

### AMD US (`AMD_US_Equity`)

- Model numbers, header figures as drawn (capture 024): Price USD 645.86, Market cap USD 1.05T (as of October 8th, 2026), Enterprise value USD 1.05T, Net debt USD -6.71B, Beta 1.55, Average volume 20.41M, Short interest 2.5%; footer "October 8th, 2026, 9:02a ET | Source: Bloomberg." Model tab (capture 027; `data/run3/fwd1/AMD_model_tab.json`): two tables, a version comparison ("Figure | Before, October 7th, 2026 | After, October 8th, 2026 | Change | Change, % | Detail ...", 9 rows; first row the consensus price/earnings ratio for fiscal year 2026, 86.8x to 86.3x) and "Consensus (Bloomberg) | Financial Summary" with fiscal-year columns 2016 to 2025, 65 rows.
- Business description (captures 024, 026): company line at the top ends in an ellipsis ("... as well as provides assembling, testing, and..."); "About the company" opened, quoted "Advanced Micro Devices, Inc. (AMD) produces semiconductor products and devices. The Company offers products such as microprocessors, embedded microprocessors, chipsets, graphics, video and multimedia products and supplies it to third-party foundries, as well as provides assembling, testing, and packaging services. AMD serves customers worldwide." with "Company description from Bloomberg".
- **Where a segment breakdown would be** (capture 025; `data/run3/fwd1/AMD_segments_dom.json`): the panel `data-segment-state="REASON"`, 0 rows, 0 tables, 0 headings, under "Business segments -- from the filing", reading: "No filing analysis is stored for this name yet, so no segment breakdown is shown. A segment table with figures needs a separate segment data pull." **The page does not draw the served segment table; it draws that reason.**
- API client, key `segment_table` (`data/run3/fwd1/AMD_segment_table_api.json`): `status` "served"; rows 6 ("Data Center" level 1 first value 16635; "Client & Gaming" 1 14550; "Client" 2 10640; "Gaming" 2 3910; "Embedded" 1 3454; "All Other" 1 null); first row name "Data Center", first value 16635; `periods[0].label` "Fiscal year 2025"; `currency` "USD"; `units` "millions"; `period_note` "A column is named with a fiscal year where its top-level rows add up to the company's reported revenue for that year. The other columns keep Bloomberg's own period numbers."
- Beside it (read in passing, not asked): ASML NA's `segment_table` also reads `status` "served", 12 rows, first "Net System", while the page draws "...so no segment breakdown is shown" for ASML (capture 013). BA and NU `segment_table` read `status` "none", 0 rows.

## FWD-7

DONE WHEN (quoted, v0.41 lines 549-551): "EXERCISED -- (v0.39) a seat opens the one place on demand, sees every covered company with its last-refreshed date, and finds a stale one without opening any folders. Adam's own use stays the ACCEPT".

- First visit: `/freshness` was the first page opened after the sign-in landing on `/market`. 95 rows; columns Company, Oldest input, Bloomberg, Seeking Alpha, Research pack, Stale (the header reads "Seeking Alpha"). Summary: "1 of 95 covered companies have an input older than 7 trading days." Page end: "End of Freshness. Data as of October 8th, 2026, 5:00p ET." Captures 001 (top), 012 (second visit top).
- **First-paint time** (navigation start to first table row; `data/run3/fwd7/dom_first.json`, `dom_second.json`): first visit 2,093 ms (DOMContentLoaded 224 ms); second visit in the same session 1,618 ms (DOMContentLoaded 221 ms). Earlier passes of this worker, for comparison only: pass 1 first 3,688 ms / second 1,581 ms; pass 2 first 1,633 ms / second 1,576 ms. Round 78 read 4,580 / 2,019 ms.
- **Rows the page flags stale: 1 of 95**, "Lenovo 992 HK" ("Seeking Alpha last read 2026-09-22"). The API client's `stale` reads true for the same one row and no other.
- **Ten Seeking Alpha cells** (page cell exactly as drawn / the cell's state attribute; then the API client's `seeking_alpha.state` and `.sentence`; captures 002-011, one per row in the order listed). The page draws none of the three sentences' words on any row (`page_draws_api_sentence` false for 10 of 10):
  | # | row | page draws | API `state` | API `sentence` |
  |---|---|---|---|---|
  | 1 | Boeing BA | `2026-10-07` (collected) | read | Seeking Alpha last read 2026-10-07. |
  | 2 | Alibaba BABA | `2026-10-06` (collected) | read | Seeking Alpha last read 2026-10-06. |
  | 3 | Costco COST | `2026-10-07` (collected) | read | Seeking Alpha last read 2026-10-07. |
  | 4 | AIA Group | `Not collected` | no_record | No Seeking Alpha collection record is held for this company yet. |
  | 5 | ServiceNow NOW US | `Not collected` | no_record | No Seeking Alpha collection record is held for this company yet. |
  | 6 | Zurich Insurance ZURN SW | `Not collected` | no_record | No Seeking Alpha collection record is held for this company yet. |
  | 7 | Hon Hai 2317 TT | `Not collected` | checked | Seeking Alpha was checked on 2026-10-05 and no article is held for this company. |
  | 8 | Monster MNST | `Not collected` | checked | Seeking Alpha was checked on 2026-10-08 and no article is held for this company. |
  | 9 | Lenovo 992 HK | `2026-09-22` (stale) | read | Seeking Alpha last read 2026-09-22. |
  | 10 | KDDI | `Not collected` | checked | Seeking Alpha was checked on 2026-10-05 and no article is held for this company. |
  Six of the ten read without a date (rows 4-8 and 10); four carry a date (rows 1-3 and 9). On the page, `no_record` and `checked` rows draw the same word, "Not collected".
- Over all 95 rows (API client, `data/run3/api/freshness_rows.json`): `read` 13, `checked` 15, `no_record` 67.

## SECTIONS

Order text: "this round the server sends five stored sections of the team's notes on /thesis (company description, why we own, positives, negatives, special items) under the key `dossier_sections`." (No PRD DONE WHEN line is named by the order for this act.)

- **ASML NA and NU: the page draws none of the five** as a section, under any heading. After the Thesis tab loads and after opening the closed disclosure "Posture, research dossier and readings" (captures 014/015 ASML closed/open, 028/029 NU closed/open; `data/run3/sections/ASML_page_scan.json`, `NU_page_scan.json`): the headings "Company description", "Why we own", "Positives", "Negatives" and "Special items" occur 0 times as a heading or text, with one exception: the words "Company description from Bloomberg" occur as a source caption in the "About the company" block (not a section). The disclosure holds the Posture line, "No fund of record", the Chatter and Breakout readings (ASML: "Collected this month: 2", "Breakout (price) #10 | +6.36% over the last 30 days"; NU: "No articles collected for this name this month.", "#7 | +10.65% over the last 30 days") and the readings footer. The Thesis tab's own text for ASML is the two "research team's thesis pillars" ("Secular growth tailwinds trump short-term cyclicality in this trillion dollar market"; "Monopoly in EUV lithography with an impregnable moat") with "Source: ASML research pack 5_5_2026" and the three cards.
- API client, key `dossier_sections` (5 entries each; `status`, then the first 80 characters of `text`, or of `reason` where absent; non-ASCII shown as `\u` escapes):
  - ASML NA: `company_description` served "COMPANY DESCRIPTION:What started as a failing joint venture between ASM Internat"; `why_we_own` served "Why we own ASML is the sole supplier of one of the most critical tools in the en"; `positives` served "Positives - Total net sales of \u20ac9.3B were above the \u20ac8.4-9.0B guided range, up 2"; `negatives` served "Negatives - Shares fell 3.8% following the print despite the beat-and-raise, ref"; `special_items` served "Special items: ASMLhas granted a \u201cstichting\u201d, or preference share option, to a D".
  - NU: `company_description` absent "The research update of 2026-Q2 has no \"Company description\" section."; `why_we_own` served "Why we own Nu is the largest digital bank in Latin America, operating under the "; `positives` served "Positives - First-ever $1B net-income quarter, with net income reaching $1.06bn,"; `negatives` served "Negatives - Management noted macro caution in Brazil requiring vigilance on cons"; `special_items` absent "The research update of 2026-Q2 has no \"Special items\" section."
  - Each entry carries the keys `field`, `heading`, `status`, `text`, `reason`, `citation`; the headings read "Company description", "Why we own it", "Positives", "Negatives", "Special items".
- The server serves a value the page does not draw: a finding for the page's owner, not a failure of the walk.

## Not walked

Nothing named by the order was left unwalked. Not walked outside the order: the non-Dev negative arm (the account is Dev only), any role-gated view, and the ASML NA Risks and Recommendation windows' passages beyond their text (read, not pressed).

## Cleanup

Walker `status` after pass 3: `armed=no armedBy=none; SSM ABSENT`. Dev server stopped by this worker (its own process tree, by pid); listeners on port 5174 read 0 afterwards.
